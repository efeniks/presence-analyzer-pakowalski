# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from flask import redirect, abort

from presence_analyzer.main import app
from presence_analyzer.utils import (
    jsonify,
    get_data,
    mean,
    group_by_weekday,
    interval,
    seconds_since_midnight,
    mean_date
)
import datetime

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect('/static/presence_weekday.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = get_data()
    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
        for i in data.keys()
    ]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def presence_start_end_view(user_id):
    """

    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    start_list = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    for start in data[user_id].keys():
        start1 = data[user_id][start]['start']
        for i in range(0, 6):
            if start.weekday() == i:
                for j in range(1, 7):
                    if i == j - 1:
                        start_list[j].append(seconds_since_midnight(start1))

    end_list = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
    for end in data[user_id].keys():
        end1 = data[user_id][end]['end']
        for i in range(0, 6):
            if end.weekday() == i:
                for j in range(1, 7):
                    if i == j - 1:
                        end_list[j].append(seconds_since_midnight(end1))

    result = [["Mon", mean_date(start_list[1]), mean_date(end_list[1])],
              ["Tue", mean_date(start_list[2]), mean_date(end_list[2])],
              ["Wed", mean_date(start_list[3]), mean_date(end_list[3])],
              ["Thu", mean_date(start_list[4]), mean_date(end_list[4])],
              ["Fri", mean_date(start_list[5]), mean_date(end_list[5])],
              ["Sat", mean_date(start_list[6]), mean_date(end_list[6])],
              ["Sun", mean_date(start_list[7]), mean_date(end_list[7])],
              ]
    return result
