# Python Mastery — L3 Internals

This file explains how to run the L3 knowledge tasks from the terminal.

## 1. Open the project folder

```bash
cd "TASKS/L3 INTERNALS/KNOWLEDGE_L3"
```

If your terminal already shows `KNOWLEDGE_L3`, skip this command.

## 2. Run one task

Use the task ID after the Python filename.

```bash
python knowledge_l3.py l3-002
```

Examples:

```bash
python knowledge_l3.py l3-009
python knowledge_l3.py l3-010
python knowledge_l3.py l3-011
python knowledge_l3.py l3-012
```

## 3. Run all completed tasks

```bash
python knowledge_l3.py all
```

## 4. Show available commands

```bash
python knowledge_l3.py --help
```

## Task IDs

| Task ID | Topic |
|---|---|
| `l3-002` | CPython Internals |
| `l3-003` | Memory Management |
| `l3-004` | Descriptors |
| `l3-005` | Metaclasses |
| `l3-006` | `__slots__` |
| `l3-007` | Concurrency Models |
| `l3-008` | Threading |
| `l3-009` | Multiprocessing |
| `l3-010` | AsyncIO |
| `l3-011` | Profiling |
| `l3-012` | Advanced Typing and Protocol |

## Common error

If Python says the file does not exist, check your current folder:

```bash
pwd
ls
```

Make sure `knowledge_l3.py` appears in the `ls` output.
