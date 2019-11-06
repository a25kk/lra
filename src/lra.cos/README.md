# LRA Consulting on Schedule

## Package providing event tool to manage consultation appointments

* `Source code @ GitHub <https://github.com/potzenheimer/lra.cos>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

It contains content types to manage consultation appointments and a consulting on
schedule tool that allows for appointment date management and booking.

### Features included

* Content Types
* Appointment management
* Appointment booking form
* Appointment storage and availability

## Installation

To install `lra.cos` you simply add ``lra.cos``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `lra.cos` using the Add-ons control panel.

## Note

The package uses an external RDB to store appointment dates and manage 
bookings