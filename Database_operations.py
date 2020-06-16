#!/usr/bin/env python3

import pprint
import collections
from Chinook_Python import *
from collections import namedtuple


def project(relation, columns):
    newTuple = collections.namedtuple('project',columns)
    newset = set()
    for i in relation:
        arrCol = []
        for j in columns:
            arrCol.append(getattr(i,j))
        obj = newTuple(*arrCol)
        newset.add(obj)
    return newset


def select(relation, predicate):
    newset = set()
    for i in relation:
        #print(predicate(i))
        if(predicate(i)):
            newset.add(i)
    return newset


def rename(relation, new_columns=None, new_relation=None):
    # print(relation._fields)
    Result = collections.namedtuple('Results',new_columns)
    newset = set()
    for i in relation:
        if(len(new_columns) == len(i._fields)):
            obj = Result(*i)
            newset.add(obj)
    return newset


def cross(relation1, relation2):
    newset = set()
    for i in relation1:
        for j in relation2:
            New = collections.namedtuple('New', i._fields+j._fields)
            obj = New(*i,*j)
            newset.add(obj)
    return newset


def theta_join(relation1, relation2, predicate):
    newset = set()
    for i in relation1:
        for j in relation2:
            New = collections.namedtuple('New', i._fields+j._fields)
            obj = New(*i,*j)
            if(predicate(i,j)):
                newset.add(obj)
    return newset


# def natural_join(relation1, relation2):
#     for i in relation1:
#         for j in relation2:
#             intersection_field = set(i._fields).intersection(set(j._fields))
#             natural_join = collections.namedtuple('NaturalJoin', set(i._fields).union(set(j._fields)))
#             for column in intersection_field:
#                 # getattr(i,column)
#                 obj = natural_join(set(i).union(set(j)))
#                 print(obj)


pprint.pprint(
    project(
        select(
            select(
                cross(
                    Album,
                    rename(Artist, ['Id', 'Name'])
                ),
                lambda t: t.ArtistId == t.Id
            ),
            lambda t: t.Name == 'Red Hot Chili Peppers'
        ),
        ['Title']
    )
)

pprint.pprint(
    project(
        select(
            theta_join(
                Album,
                rename(Artist, ['Id', 'Name']),
                lambda t1, t2: t1.ArtistId == t2.Id
            ),
            lambda t: t.Name == 'Red Hot Chili Peppers'
        ),
        ['Title']
    )
)

pprint.pprint(
    project(
        theta_join(
            Album,
            rename(
                select(Artist, lambda t: t.Name == 'Red Hot Chili Peppers'),
                ['Id', 'Name']
            ),
            lambda t1, t2: t1.ArtistId == t2.Id
        ),
        ['Title']
    )
)

# pprint.pprint(
#     project(
#         natural_join(
#             Album,
#             select(Artist, lambda t: t.Name == 'Red Hot Chili Peppers')
#         ),
#         ['Title']
#     )
# )
