# SIMPL-Cases
Tiny script to compare SIMPL test outputs to supplied test cases.

## Requirements
- Python 3.10
- SIMPL Project :P

## Instructions
- Make a new folder (or use an existing one) in the root of the project called `tests`

![image](https://user-images.githubusercontent.com/32196181/133342484-49afa4fc-cb4d-4392-87ce-27a835bf33b6.png)
- Place extracted folders from the Official Test Cases (ie. `01_scanner` and `02_parser`) in the `tests` folder

![image](https://user-images.githubusercontent.com/32196181/133342712-6a2763ba-9e00-4bb4-a417-919a0ca8a617.png)
- Place `testcases.py` in the `tests` folder, too

![image](https://user-images.githubusercontent.com/32196181/133342744-f65baee2-e0e8-4847-9142-d0a49b7926f4.png)
- Run the following command from within the `tests` folder:

```bash
$ python3.10 testcases.py scanner
```
- wherein `scanner` can be substituted by any of the following
  * `parser` (tests parser)
  * `all` (tests scanner and parser)
  * `compile` (only tests to see if testscanner and testparser can compile)
