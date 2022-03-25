#!/usr/bin/python
# -*- coding: utf-8 -*-

# Connect To MongoDB
from hahow import Hahow
import pymongo
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client.social_media

# Initialize Hahow Browser
h = Hahow()

# Collect Courses
courses = h.collectCouses('/courses?page=1&order=NUM_OF_STUDENT&status=PUBLISHED', 10)
for course in courses:
    # Collect Students in Discussion Forum
    h.collectDiscussions(course)

    # Save To MongoDB
    id = course.save(db.hahow).inserted_id

    print(id)
    print('=' * 10)


