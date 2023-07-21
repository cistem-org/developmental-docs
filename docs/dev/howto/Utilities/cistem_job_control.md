# cisTEM Job Control

This diagram shows the rough sequence of events when a cisTEM job is run through the GUI.
The messages shown in bold are 16-byte control codes defined in `socket_codes.h`. These are usually followed by 16 bytes of information,
which often encodes the number of bytes of other results to follow (Shown in italics)

[assets/img/cisTEM_job_control.png]