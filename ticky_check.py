#!/usr/bin/env python3

import re
import operator
import csv


def organise_data():
	error = {}
	per_user_error = {}
	per_user_info = {}
	with open('syslog.log') as logfile:
		for line in logfile.readlines():
			username = re.search(r'\((.*)\)', line).group(1)
			result_error = re.search(r'ticky: ERROR ([\w ]*) ', line)
			result_info = re.search(r'ticky: INFO ([\w ]*) ', line)
			if result_error != None:
				error[result_error.group(1)] = error.get(result_error.group(1), 0) + 1
				per_user_error[username] = per_user_error.get(username, 0) + 1
			if result_info != None:
				per_user_info[username] = per_user_info.get(username, 0) + 1
	return error, per_user_error, per_user_info


def sort_data(data):
	error, per_user_error, per_user_info = data
	error_sorted = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
	per_user_error_sorted = dict(sorted(per_user_error.items()))
	per_user_info_sorted = dict(sorted(per_user_info.items()))
	usernames = list(per_user_error_sorted)
	usernames.extend(list(per_user_info_sorted))
	username_list = sorted(set(usernames))
	return error_sorted, per_user_error_sorted, per_user_info_sorted, username_list


def write_data_csv(error, per_user_error, per_user_info, username_list):
	# writing the errors to a csv file with headers included
	with open('error_message.csv', mode='w') as file:
		fieldnames = ['Error', 'Count']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		for key in error:
		       writer.writerow({'Error': key[0], 'Count': key[1]})


	with open('user_statistics.csv', mode='w') as file:
		fieldnames = ["Username", "INFO", "ERROR"]
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		usernames = username_list
		for username in username_list:
			writer.writerow({'Username': username, 'INFO': per_user_info.get(username, 0),
				'ERROR': per_user_error.get(username, 0)})


if __name__ == '__main__':
		data = organise_data()
		error_sorted, per_user_error_sorted, per_user_info_sorted, username_list = sort_data(data)
		write_data_csv(error_sorted, per_user_error_sorted, per_user_info_sorted, username_list)
