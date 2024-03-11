# Steffim


| ![Stef over time](https://raw.githubusercontent.com/schicho/steffim/master/generated/stef_over_time.svg) | ![Chair ranking](https://raw.githubusercontent.com/schicho/steffim/master/generated/stef_by_chair.svg) |
|---|---|

How many Stefanies, Stephans, Stefans, Steffis, and so on are working at the faculty of computer science and mathematics (german abbreviation: FIM) at the University of Passau?

Started as a joke, when both a friend of mine and I noticed we have a lot of 'Stef' colleagues, this project is now a serious attempt to answer this question - continuously.

## How does it work?

A script is run monthly on github actions.
It crawls the FIM chair overview page and finds the public list of employees for each chair.
It then counts the number of employees with a name starting with 'Stef' or 'Steph' and generates both a graph over time and a chair ranking.

You can hotlink the images with the following URLs to have automatic updates:

* https://raw.githubusercontent.com/schicho/steffim/master/generated/stef_over_time.svg
* https://raw.githubusercontent.com/schicho/steffim/master/generated/stef_by_chair.svg
