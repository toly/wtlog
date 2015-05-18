# WTLog

## Description

WTLog - python script for auto logging work time.

## Install and init

Install

	git clone https://github.com/toly/wtlog.git
	cd wtlog
	sudo python.py install
	
Init

	wtlog.py -i
	
Add to crontab line:

	* * * * * wtlog.py -l

## Usage

For show today statistics: 

	wtlog.py -r
	
For show another day statistics:

	wtlog.py -r -d 2015.05.10
