#!/usr/bin/python
# -*- coding: utf-8 -*-
from browser import Browser
from course import Course

class Hahow:

    def __init__(self):
        self._hahow = Browser('https://hahow.in', 5)

    def collectCouses(self, path, sizeOfCourses = 100):
        courses = []
        page = self._hahow.goto(path)
        while len(courses) < sizeOfCourses:
            # List all courses
            courseList = page.find('div', {'class': 'list-container'})
            courses = [self.createCourse(linkTag) for linkTag in courseList.find_all('a', href=True)]

            # Go to next Course List Page
            pageList = page.find('div', {'class': 'pagination-container'})
            courseListTags = pageList.find_all('a', href=True)
            nextCourseListTag = courseListTags.pop()
            page = self._hahow.goto(nextCourseListTag['href'])
            return courses

    def createCourse(self, linkTag):
        course = Course(linkTag['href'])
        courseStatusBar = linkTag.find('div', {'class': 'course-status-bar'})
        ratingTags = courseStatusBar.find_all('span', {'class': 'rwd-rating'})
        course.setRating(ratingTags[1].get_text())
        cost = courseStatusBar.find('span', {'class': 'text-secondary'})
        course.setCost(cost.get_text())
        return course

    def expandDiscussionList(self):
        page = None
        while(True):
            page = self._hahow.scrollDown()
            mainDiv = page.find('div', {'class': 'layout-main-wrap'})
            more = mainDiv.find('div', {'class': 'text-center'})
            if(more is None):
                break;
            self._hahow.click(more.find('button'))
        return page

    def collectDiscussions(self, course):
        page = self._hahow.goto(course.getPath() + '/discussions')
        titleTag = page.find('h1', {'class': 'title'})
        course.setTitle(titleTag.get_text())
        enrollmentDiv = page.find('div', {'data-for': 'enrollment'})
        course.setEnrollment(enrollmentDiv.find('span', {'class': 'sign-desc'}).get_text())
        lengthDiv = page.find('div', {'data-for': 'course-length'})
        course.setLength(lengthDiv.find('span', {'class': 'sign-desc'}).get_text())

        discussList = []
        page = self.expandDiscussionList()
        allDiscussions = page.find_all('div', {'class': 'discussion'})
        for discuss in allDiscussions:
            user = discuss.find('a', {'class': 'username'})
            course.addStudent(user.get_text(), user['href'])
        return course 
