# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from flask import redirect, abort

from presence_analyzer.main import app
from presence_analyzer.utils import (
    jsonify, get_data, mean, group_by_weekday, interval, seconds_since_midnight,
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

    starts = data[user_id].keys()
    ends = data[user_id].keys()
    start_list_1 = []
    start_list_2 = []
    start_list_3 = []
    start_list_4 = []
    start_list_5 = []
    start_list_6 = []
    start_list_7 = []
    for start in starts:
        start1 = data[user_id][start]['start']
        if start.weekday() == 0:
            start_list_1.append(seconds_since_midnight(start1))
        elif start.weekday() == 1:
            start_list_2.append(seconds_since_midnight(start1))
        elif start.weekday() == 2:
            start_list_3.append(seconds_since_midnight(start1))
        elif start.weekday() == 3:
            start_list_4.append(seconds_since_midnight(start1))
        elif start.weekday() == 4:
            start_list_5.append(seconds_since_midnight(start1))
        elif start.weekday() == 5:
            start_list_6.append(seconds_since_midnight(start1))
        elif start.weekday() == 6:
            start_list_7.append(seconds_since_midnight(start1))

    end_list_1 = []
    end_list_2 = []
    end_list_3 = []
    end_list_4 = []
    end_list_5 = []
    end_list_6 = []
    end_list_7 = []
    for end in ends:
        end1 = data[user_id][end]['end']
        if end.weekday() == 0:
            end_list_1.append(seconds_since_midnight(end1))
        elif end.weekday() == 1:
            end_list_2.append(seconds_since_midnight(end1))
        elif end.weekday() == 2:
            end_list_3.append(seconds_since_midnight(end1))
        elif end.weekday() == 3:
            end_list_4.append(seconds_since_midnight(end1))
        elif end.weekday() == 4:
            end_list_5.append(seconds_since_midnight(end1))
        elif end.weekday() == 5:
            end_list_6.append(seconds_since_midnight(end1))
        elif end.weekday() == 6:
            end_list_7.append(seconds_since_midnight(end1))

    mean_start_1 = mean_date(start_list_1)
    mean_end_1 = mean_date(end_list_1)
    mean_start_2 = mean_date(start_list_2)
    mean_end_2 = mean_date(end_list_2)
    mean_start_3 = mean_date(start_list_3)
    mean_end_3 = mean_date(end_list_3)
    mean_start_4 = mean_date(start_list_4)
    mean_end_4 = mean_date(end_list_4)
    mean_start_5 = mean_date(start_list_5)
    mean_end_5 = mean_date(end_list_5)
    mean_start_6 = mean_date(start_list_6)
    mean_end_6 = mean_date(end_list_6)
    mean_start_7 = mean_date(start_list_7)
    mean_end_7 = mean_date(end_list_7)
    result = [["Mon", mean_start_1, mean_end_1],
              ["Tue", mean_start_2, mean_end_2],
              ["Wed", mean_start_3, mean_end_3],
              ["Thu", mean_start_4, mean_end_4],
              ["Fri", mean_start_5, mean_end_5],
              ["Sat", mean_start_6, mean_end_6],
              ["Sun", mean_start_7, mean_end_7],
              ]
    return result
