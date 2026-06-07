# CONSTRAINTS — How to Use the Constraints Database

## Overview
MJ's hard scheduling limits live in the Constraints database on the Dashboard page in Notion (ID: 36520c51-aebe-80bd-8f09-da0d11785980). Claude queries this database at the start of every session. This file explains how to enforce that data.

## How to Enforce Constraints
Each row in the Constraints database is a hard limit. Claude must never override these for any reason. If a scheduling request conflicts with a constraint, flag it to MJ and ask how to handle it — do not proceed around it.

If the Constraints database is empty, there are currently no hard limits in place. This is intentional — do not assume the database is incomplete.
