#!/bin/bash
# Migration script to preserve Jupyter Book and create new documentation structure
set -e

echo "=== cisTEM Documentation Migration Script ==="
echo "This script will:"
echo "1. Preserve ALL existing Jupyter Book content in initial_jupyter_book_impl/"
echo "2. Create new documentation system structure"
echo "3. Set up MkDocs configuration"
echo ""
read -p "Press Enter to continue or Ctrl+C to abort..."

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Create new branch for migration
MIGRATION_BRANCH="migration/new-doc-system-$(date +%Y%m%d)"
echo "Creating migration branch: $MIGRATION_BRANCH"
git checkout -b "$MIGRATION_BRANCH"

# Create the preservation directory
echo "Creating initial_jupyter_book_impl/ directory..."
mkdir -p initial_jupyter_book_impl

# Move all existing content to preservation directory
echo "Preserving existing Jupyter Book content..."
for item in *; do
    if [ "$item" != "initial_jupyter_book_impl" ] && [ "$item" != ".git" ] && [ "$item" != ".github" ]; then
        echo "  Moving: $item"
        git mv "$item" initial_jupyter_book_impl/ 2>/dev/null || mv "$item" initial_jupyter_book_impl/
    fi
done

# Move .github workflows too (we'll create new ones later)
if [ -d ".github" ]; then
    echo "  Preserving .github workflows..."
    git mv .github initial_jupyter_book_impl/ 2>/dev/null || mv .github initial_jupyter_book_impl/
fi

# Create new directory structure
echo "Creating new documentation structure..."
mkdir -p api
mkdir -p tutorials
mkdir -p llm
mkdir -p scripts
mkdir -p .ast_cache

# Create initial README for each directory
echo "# API Documentation

Auto-generated API documentation from C++ source code using AST parsing.
" > api/README.md

echo "# Tutorials

User-facing tutorials and guides.

See \`initial_jupyter_book_impl/\` for previous tutorial content.
" > tutorials/README.md

echo "# LLM-Optimized Documentation

This directory contains documentation optimized for LLM consumption:
- Token-aware chunking
- Semantic embeddings
- Structured JSON schemas
" > llm/README.md

echo "# Documentation Generation Scripts

Scripts for:
- \`parse_cpp_ast.py\` - C++ AST parsing with libclang
- \`generate_docs.py\` - Documentation page generation
- \`build_index.py\` - Search index creation
- \`update_tags.py\` - Automated tagging system
" > scripts/README.md

# Create MkDocs configuration
echo "Creating MkDocs configuration..."
cat > mkdocs.yml << 'EOF'
site_name: cisTEM Documentation
site_description: User-friendly software for cryo-EM image processing
site_author: The cisTEM Community
site_url: https://cistem-org.github.io/developmental-docs/

theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

nav:
  - Home: index.md
  - API Reference: api/
  - Tutorials: tutorials/
  - LLM Interface: llm/
  - Previous Docs (Jupyter Book): initial_jupyter_book_impl/

plugins:
  - search
  - tags:
      tags_file: tags.md

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - admonition
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true

extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/cistem-org
EOF

# Create main index page
cat > index.md << 'EOF'
# cisTEM Documentation

Welcome to the cisTEM documentation system.

[*cis*TEM](https://cistem.org) is user-friendly software to process cryo-EM images of macromolecular complexes and obtain high-resolution 3D reconstructions from them.

## Documentation Sections

### [API Reference](api/)
Auto-generated API documentation from C++ source code.

### [Tutorials](tutorials/)
Step-by-step guides for using cisTEM.

### [LLM Interface](llm/)
LLM-optimized documentation with structured schemas.

### [Previous Documentation](initial_jupyter_book_impl/)
Original Jupyter Book documentation (preserved for reference).

## Getting Started

- New users: See the [tutorials](tutorials/)
- Developers: Check the [API reference](api/)
- For the original documentation: Visit [initial_jupyter_book_impl](initial_jupyter_book_impl/)

## About This Documentation System

This documentation is built using:
- **MkDocs Material** for the static site
- **libclang** for C++ AST parsing
- **Automated tagging** for easy navigation
- **LLM optimization** for AI-assisted development
EOF

# Create tags page
cat > tags.md << 'EOF'
# Documentation Tags

Browse documentation by topic:

[TAGS]
EOF

# Create requirements.txt for documentation building
cat > requirements.txt << 'EOF'
mkdocs>=1.5.0
mkdocs-material>=9.0.0
pymdown-extensions>=10.0
mkdocs-git-revision-date-localized-plugin
mkdocs-minify-plugin
mike
EOF

# Create .gitignore for new structure
cat > .gitignore << 'EOF'
# MkDocs
site/
.cache/

# AST cache
.ast_cache/*.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF

# Restore .github for GitHub Pages (create minimal version)
mkdir -p .github/workflows
cat > .github/workflows/deploy-docs.yml << 'EOF'
name: Deploy Documentation

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Build documentation
        run: mkdocs build --strict

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
EOF

# Stage all changes
echo "Staging all changes..."
git add -A

# Show what will be committed
echo ""
echo "=== Changes to be committed ==="
git status

echo ""
echo "=== Summary ==="
echo "✓ All existing content preserved in: initial_jupyter_book_impl/"
echo "✓ New structure created: api/, tutorials/, llm/, scripts/"
echo "✓ MkDocs configuration created"
echo "✓ GitHub Actions workflow created"
echo ""
echo "Branch: $MIGRATION_BRANCH"
echo ""
echo "Next steps:"
echo "1. Review the changes with: git diff --staged"
echo "2. Commit with: git commit -m 'Migrate to new documentation system, preserve Jupyter Book'"
echo "3. Push with: git push -u origin $MIGRATION_BRANCH"
echo "4. Test locally with: mkdocs serve"
