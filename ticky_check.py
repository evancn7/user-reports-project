#!/usr/bin/env python3

import re
import operator
import csv


def compile_data():
	errors = {}
	user_stats = {}
	with open('syslog.log') as file:
		for line in file.readlines():
			result = re.search(r"ticky: ([\w]*) ([\w ']*).*\(([\w. ]*)\)", line)
			log_type = result.group(1)
			log_detail = result.group(2)
			username = result.group(3)
			if log_type == 'INFO':
				val = user_stats.get(username, [0, 0])
				val[0] += 1
				user_stats[username] = val
			if log_type == 'ERROR':
				val = user_stats.get(username, [0, 0])
				val[1] += 1
				user_stats[username] = val
				errors[log_detail] = errors.get(log_detail, 0) + 1
	return sort_errors(errors), sort_users(user_stats)


def sort_errors(dictionary):
	"""takes in dictionary sorts it in descending order on values and returns tuple"""
	result = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
	result.insert(0, ('Error', 'Count'))
	return result


def sort_users(dictionary):
	"""takes in dictionary sorts it by key in alphabetical order and returns tuple"""
	result = sorted(dictionary.items())
	result.insert(0, ('Username', ['INFO', 'ERROR']))
	return result


def write_csv(errors, user_stats):
		with open('error_message.csv', mode='w') as file:
			writer = csv.writer(file)
			for data in errors:
				writer.writerow(data)
		with open('user_statistics.csv', mode='w') as file:
			writer = csv.writer(file)
			for data in user_stats:
				writer.writerow([data[0], data[1][0], data[1][1]])


if __name__ == '__main__':
	errors = compile_data()[0]
	user_stats = compile_data()[1]
	write_csv(errors, user_stats)

