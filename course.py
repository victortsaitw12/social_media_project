#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

class Course:
    def __init__(self, path):
        self._course = {
          'path': path,
          'title': '',
          'enrollment': 0,
          'length': 0,
          'rating': '',
          'cost': 0,
          'students': {}
        }

    def getPath(self):
        return self._course['path']

    def setTitle(self, title):
        self._course['title'] = title

    def setEnrollment(self, enrollment):
        self._course['enrollment'] = enrollment

    def setLength(self, length):
        self._course['length'] = length

    def setRating(self, rating):
        self._course['rating'] = rating

    def setCost(self, cost):
        self._course['cost'] = cost

    def __str__(self):
        return json.dumps(self._course)

    def addStudent(self, name, url):
        self._course['students'][url] = name

    def save(self, db):
        return db.insert_one(self._course)
