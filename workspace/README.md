# SolPOC Optimizer workspace

This directory contains the editable files and generated results
used by SolPOC Optimizer.

## manual_interface

Contains editable copies of the experiment templates.

You may modify the parameters directly in these files without
changing the installed package.

## new_functions

Contains editable copies of the additional Python functions used
by the scheduler.

The scheduler loads these external copies in priority.

## Other directories

- plan_experience: plans waiting to be executed
- plan_executer: successfully executed plans
- plan_failed: plans that could not be executed
- runs: experiment results
