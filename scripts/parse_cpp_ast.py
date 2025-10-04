#!/usr/bin/env python3
"""
parse_cpp_ast.py - C++ AST Parser for cisTEM Documentation System

Extracts structured metadata from C++ source files using libclang.
Handles:
- Classes, functions, methods
- CUDA kernels (__global__, __device__, __host__)
- Template classes and specializations
- Documentation comments
- Incremental parsing with caching
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

import clang.cindex
from clang.cindex import CursorKind, TypeKind


class CppASTParser:
    """Parse C++ source files and extract structured metadata."""

    def __init__(
        self,
        cache_dir: str = ".ast_cache",
        include_paths: Optional[List[str]] = None,
        defines: Optional[List[str]] = None,
    ):
        """
        Initialize the AST parser.

        Args:
            cache_dir: Directory for caching parsed results
            include_paths: List of include directories
            defines: List of preprocessor defines
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize libclang
        try:
            clang.cindex.Config.set_library_path(os.environ.get('CLANG_LIBRARY_PATH', '/usr/lib/llvm-14/lib'))
        except Exception:
            pass  # Already configured or will use default

        self.index = clang.cindex.Index.create()

        # Build compilation arguments
        self.compile_args = [
            '-std=c++17',
            '-x', 'c++',
        ]

        # Add include paths
        if include_paths:
            for path in include_paths:
                self.compile_args.extend(['-I', path])

        # Add defines
        if defines:
            for define in defines:
                self.compile_args.append(f'-D{define}')

        # cisTEM-specific includes and defines
        self.compile_args.extend([
            '-I/usr/include',
            '-I./include',
            '-I./src',
            '-DHAVE_MKL',
            # Suppress some warnings that clutter output
            '-Wno-pragma-once-outside-header',
        ])

    def _get_file_hash(self, filepath: Path) -> str:
        """Compute hash of file contents for cache invalidation."""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _get_cache_path(self, file_hash: str) -> Path:
        """Get cache file path for given file hash."""
        return self.cache_dir / f"{file_hash}.json"

    def parse_file(self, filepath: str, force: bool = False) -> Dict:
        """
        Parse a C++ source file and extract metadata.

        Args:
            filepath: Path to the C++ file
            force: Force re-parse even if cached

        Returns:
            Dictionary containing extracted metadata
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        # Check cache
        file_hash = self._get_file_hash(filepath)
        cache_file = self._get_cache_path(file_hash)

        if not force and cache_file.exists():
            print(f"  [cache hit] {filepath.name}")
            with open(cache_file) as f:
                return json.load(f)

        print(f"  [parsing] {filepath.name}")

        # Parse with libclang
        try:
            tu = self.index.parse(
                str(filepath),
                args=self.compile_args,
                options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
            )
        except Exception as e:
            print(f"  [ERROR] Failed to parse {filepath}: {e}", file=sys.stderr)
            return self._empty_result(filepath, file_hash, error=str(e))

        # Check for parse errors
        diagnostics = list(tu.diagnostics)
        errors = [d for d in diagnostics if d.severity >= clang.cindex.Diagnostic.Error]
        if errors:
            print(f"  [WARNING] {len(errors)} errors in {filepath.name}")
            for err in errors[:3]:  # Show first 3
                print(f"    {err}")

        # Extract information
        result = {
            'file': str(filepath),
            'hash': file_hash,
            'classes': [],
            'functions': [],
            'methods': [],
            'templates': [],
            'cuda_kernels': [],
            'enums': [],
            'typedefs': [],
            'namespaces': set(),
            'includes': [],
            'errors': len(errors),
        }

        # Visit AST nodes
        self._visit_node(tu.cursor, result, filepath)

        # Convert sets to lists for JSON serialization
        result['namespaces'] = sorted(list(result['namespaces']))

        # Save to cache
        with open(cache_file, 'w') as f:
            json.dump(result, f, indent=2)

        return result

    def _empty_result(self, filepath: Path, file_hash: str, error: str = "") -> Dict:
        """Return empty result structure with error."""
        return {
            'file': str(filepath),
            'hash': file_hash,
            'classes': [],
            'functions': [],
            'methods': [],
            'templates': [],
            'cuda_kernels': [],
            'enums': [],
            'typedefs': [],
            'namespaces': [],
            'includes': [],
            'errors': 1,
            'parse_error': error,
        }

    def _visit_node(self, cursor, result: Dict, source_file: Path, depth: int = 0):
        """
        Recursively visit AST nodes and extract information.

        Args:
            cursor: Current AST cursor
            result: Result dictionary to populate
            source_file: Original source file (to filter nodes)
            depth: Current recursion depth
        """
        # Limit recursion depth to avoid infinite loops in complex templates
        if depth > 50:
            return

        # Only process nodes from the target file
        if cursor.location.file and Path(cursor.location.file.name) != source_file:
            return

        kind = cursor.kind

        # Extract different node types
        if kind == CursorKind.CLASS_DECL or kind == CursorKind.STRUCT_DECL:
            self._extract_class(cursor, result)
        elif kind == CursorKind.FUNCTION_DECL:
            self._extract_function(cursor, result)
        elif kind == CursorKind.CXX_METHOD:
            self._extract_method(cursor, result)
        elif kind == CursorKind.CLASS_TEMPLATE:
            self._extract_template(cursor, result)
        elif kind == CursorKind.ENUM_DECL:
            self._extract_enum(cursor, result)
        elif kind == CursorKind.TYPEDEF_DECL:
            self._extract_typedef(cursor, result)
        elif kind == CursorKind.NAMESPACE:
            if cursor.spelling:
                result['namespaces'].add(cursor.spelling)
        elif kind == CursorKind.INCLUSION_DIRECTIVE:
            self._extract_include(cursor, result)

        # Check for CUDA annotations
        self._check_cuda_kernel(cursor, result)

        # Recurse into children
        for child in cursor.get_children():
            self._visit_node(child, result, source_file, depth + 1)

    def _extract_class(self, cursor, result: Dict):
        """Extract class/struct information."""
        class_info = {
            'name': cursor.spelling,
            'kind': 'class' if cursor.kind == CursorKind.CLASS_DECL else 'struct',
            'location': self._get_location(cursor),
            'line': cursor.location.line,
            'doc': self._get_documentation(cursor),
            'bases': [],
            'methods': [],
            'fields': [],
            'access': self._get_access_specifier(cursor),
        }

        # Extract base classes
        for child in cursor.get_children():
            if child.kind == CursorKind.CXX_BASE_SPECIFIER:
                base_name = child.type.spelling
                class_info['bases'].append(base_name)

        result['classes'].append(class_info)

    def _extract_function(self, cursor, result: Dict):
        """Extract function information."""
        func_info = {
            'name': cursor.spelling,
            'location': self._get_location(cursor),
            'line': cursor.location.line,
            'return_type': cursor.result_type.spelling,
            'parameters': self._extract_parameters(cursor),
            'doc': self._get_documentation(cursor),
            'is_inline': cursor.is_inline_method(),
            'is_static': cursor.storage_class == clang.cindex.StorageClass.STATIC,
        }

        result['functions'].append(func_info)

    def _extract_method(self, cursor, result: Dict):
        """Extract class method information."""
        method_info = {
            'name': cursor.spelling,
            'class': cursor.semantic_parent.spelling if cursor.semantic_parent else None,
            'location': self._get_location(cursor),
            'line': cursor.location.line,
            'return_type': cursor.result_type.spelling,
            'parameters': self._extract_parameters(cursor),
            'doc': self._get_documentation(cursor),
            'is_const': cursor.is_const_method(),
            'is_virtual': cursor.is_virtual_method(),
            'is_pure_virtual': cursor.is_pure_virtual_method(),
            'is_static': cursor.is_static_method(),
            'access': self._get_access_specifier(cursor),
        }

        result['methods'].append(method_info)

    def _extract_template(self, cursor, result: Dict):
        """Extract template class information."""
        template_info = {
            'name': cursor.spelling,
            'location': self._get_location(cursor),
            'line': cursor.location.line,
            'parameters': [],
            'doc': self._get_documentation(cursor),
        }

        # Extract template parameters
        for child in cursor.get_children():
            if child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_info['parameters'].append({
                    'name': child.spelling,
                    'type': 'typename',
                })
            elif child.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
                template_info['parameters'].append({
                    'name': child.spelling,
                    'type': child.type.spelling,
                })

        result['templates'].append(template_info)

    def _extract_enum(self, cursor, result: Dict):
        """Extract enum information."""
        enum_info = {
            'name': cursor.spelling,
            'location': self._get_location(cursor),
            'line': cursor.location.line,
            'values': [],
            'doc': self._get_documentation(cursor),
        }

        # Extract enum values
        for child in cursor.get_children():
            if child.kind == CursorKind.ENUM_CONSTANT_DECL:
                enum_info['values'].append({
                    'name': child.spelling,
                    'value': child.enum_value,
                })

        result['enums'].append(enum_info)

    def _extract_typedef(self, cursor, result: Dict):
        """Extract typedef information."""
        typedef_info = {
            'name': cursor.spelling,
            'type': cursor.underlying_typedef_type.spelling,
            'location': self._get_location(cursor),
            'line': cursor.location.line,
        }

        result['typedefs'].append(typedef_info)

    def _extract_include(self, cursor, result: Dict):
        """Extract include directive."""
        include_file = cursor.get_included_file()
        if include_file:
            result['includes'].append(include_file.name)

    def _check_cuda_kernel(self, cursor, result: Dict):
        """Check if function is a CUDA kernel and extract info."""
        # Look for CUDA attributes in tokens
        tokens = list(cursor.get_tokens())
        cuda_attrs = []

        for token in tokens:
            if token.spelling in ['__global__', '__device__', '__host__']:
                cuda_attrs.append(token.spelling)

        if cuda_attrs and cursor.kind == CursorKind.FUNCTION_DECL:
            kernel_info = {
                'name': cursor.spelling,
                'attributes': cuda_attrs,
                'location': self._get_location(cursor),
                'line': cursor.location.line,
                'parameters': self._extract_parameters(cursor),
                'doc': self._get_documentation(cursor),
            }
            result['cuda_kernels'].append(kernel_info)

    def _extract_parameters(self, cursor) -> List[Dict]:
        """Extract function parameters."""
        params = []
        for arg in cursor.get_arguments():
            params.append({
                'name': arg.spelling,
                'type': arg.type.spelling,
            })
        return params

    def _get_documentation(self, cursor) -> Optional[str]:
        """Extract documentation comment if present."""
        comment = cursor.brief_comment
        if comment:
            return comment.strip()
        return None

    def _get_location(self, cursor) -> str:
        """Get source location as string."""
        loc = cursor.location
        return f"{loc.file.name}:{loc.line}:{loc.column}" if loc.file else f":{loc.line}:{loc.column}"

    def _get_access_specifier(self, cursor) -> str:
        """Get access specifier (public, private, protected)."""
        access = cursor.access_specifier
        if access == clang.cindex.AccessSpecifier.PUBLIC:
            return 'public'
        elif access == clang.cindex.AccessSpecifier.PRIVATE:
            return 'private'
        elif access == clang.cindex.AccessSpecifier.PROTECTED:
            return 'protected'
        return 'public'  # Default for structs


def main():
    """Command-line interface for the AST parser."""
    parser = argparse.ArgumentParser(
        description='Parse C++ source files and extract structured metadata'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='C++ source files to parse'
    )
    parser.add_argument(
        '--cache-dir',
        default='.ast_cache',
        help='Directory for caching parsed results (default: .ast_cache)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-parse even if cached'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file (default: stdout)'
    )
    parser.add_argument(
        '-I', '--include',
        action='append',
        dest='includes',
        help='Add include directory'
    )
    parser.add_argument(
        '-D', '--define',
        action='append',
        dest='defines',
        help='Add preprocessor define'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print statistics after parsing'
    )

    args = parser.parse_args()

    # Initialize parser
    ast_parser = CppASTParser(
        cache_dir=args.cache_dir,
        include_paths=args.includes,
        defines=args.defines,
    )

    # Parse all files
    results = []
    for file in args.files:
        try:
            result = ast_parser.parse_file(file, force=args.force)
            results.append(result)
        except Exception as e:
            print(f"ERROR parsing {file}: {e}", file=sys.stderr)

    # Combine results
    combined = {
        'files': results,
        'total_files': len(results),
    }

    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(combined, f, indent=2)
        print(f"\nResults written to {args.output}")
    else:
        print(json.dumps(combined, indent=2))

    # Print statistics
    if args.stats:
        print("\n=== Statistics ===", file=sys.stderr)
        total_classes = sum(len(r['classes']) for r in results)
        total_functions = sum(len(r['functions']) for r in results)
        total_methods = sum(len(r['methods']) for r in results)
        total_templates = sum(len(r['templates']) for r in results)
        total_cuda = sum(len(r['cuda_kernels']) for r in results)

        print(f"Files parsed: {len(results)}", file=sys.stderr)
        print(f"Classes: {total_classes}", file=sys.stderr)
        print(f"Functions: {total_functions}", file=sys.stderr)
        print(f"Methods: {total_methods}", file=sys.stderr)
        print(f"Templates: {total_templates}", file=sys.stderr)
        print(f"CUDA kernels: {total_cuda}", file=sys.stderr)


if __name__ == '__main__':
    main()
