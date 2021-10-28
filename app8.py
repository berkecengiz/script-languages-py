# https://www.kaggle.com/martj42/international-football-results-from-1872-to-2017

import argparse
import sys
import os.path
import xlsxwriter
import numpy as np

DATE = 0
OPP1 = 1
OPP2 = 2
SC1 = 3
SC2 = 4
EVENT = 5
CITY = 6
COUNTRY = 7
NEUTRAL = 8


def read_file(filename):
    data = []
    d_types = (str, str, str, int, int, str, str, str, bool)
    file = open(filename, 'r', encoding='utf-8')
    for line in file:
        line_tuple = tuple(t(e) for t, e in zip(d_types, line.split(",")))
        data.append(line_tuple)
    return data


def check_file(filename):
    if os.path.isfile(filename):
        extension = filename.split(".")
        if extension[1] != "csv":
            print("File is not in .csv format.")
            exit()
    else:
        print("file does not exist.")
        exit()


def avg_goals(data):
    total_goals = 0
    for entry in data:
        total_goals += entry[SC1] + entry[SC2]
    avg_g = '{0:.2f}'.format(total_goals / len(data))
    return avg_g


def document_summary(data):
    countries = []
    tournaments = []
    total_goals = 0
    total_matches = 0
    for entry in data:
        total_matches += 1
        total_goals += entry[SC1]
        total_goals += entry[SC2]
        if entry[OPP1] not in countries:
            countries.append(entry[OPP1])
        if entry[OPP2] not in countries:
            countries.append(entry[OPP2])
        if entry[EVENT] not in tournaments:
            tournaments.append(entry[EVENT])
    num_countries = len(countries)
    num_tournaments = len(tournaments)
    return total_matches, num_countries, num_tournaments, total_goals


def country_summary(data, cname):
    goals_for = 0
    goals_against = 0
    total_matches = 0
    for entry in data:
        if entry[OPP1] == cname:
            total_matches += 1
            goals_for += entry[SC1]
            goals_against += entry[SC2]

        if entry[OPP2] == cname:
            total_matches += 1
            goals_for += entry[SC2]
            goals_against += entry[SC1]
    return cname, total_matches, goals_for, goals_against


def display(data):
    summary_data = document_summary(data)
    print("Number of Matches:{} Number of Countries:{} Number of Tournaments:{} Total Goals Scored:{}"
          .format(summary_data[0], summary_data[1], summary_data[2], summary_data[3]))
    print("Average number of goals scored per match=", avg_goals(data))
    g_data = country_summary(data, "Germany")
    f_data = country_summary(data, "France")
    s_data = country_summary(data, "Spain")
    e_data = country_summary(data, "England")
    p_data = country_summary(data, "Netherlands")
    print("Summary Data for {}: Total Matches Played={} Total Goals Scored={} Total Goals Conceded={}".format(
        g_data[0], g_data[1], g_data[2], g_data[3]))
    print("Summary Data for {}: Total Matches Played={} Total Goals Scored={} Total Goals Conceded={}".format(
        f_data[0], f_data[1], f_data[2], f_data[3]))
    print("Summary Data for {}: Total Matches Played={} Total Goals Scored={} Total Goals Conceded={}".format(
        s_data[0], s_data[1], s_data[2], s_data[3]))
    print("Summary Data for {}: Total Matches Played={} Total Goals Scored={} Total Goals Conceded={}".format(
        e_data[0], e_data[1], e_data[2], e_data[3]))
    print("Summary Data for {}: Total Matches Played={} Total Goals Scored={} Total Goals Conceded={}".format(
        p_data[0], p_data[1], p_data[2], p_data[3]))


def save(data, output):
    summary_data = document_summary(data)
    avg_g = avg_goals(data)
    g_data = country_summary(data, "Germany")
    f_data = country_summary(data, "France")
    s_data = country_summary(data, "Spain")
    e_data = country_summary(data, "England")
    n_data = country_summary(data, "Netherlands")

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    align_format_1 = workbook.add_format()
    align_format_2 = workbook.add_format()
    align_format_3 = workbook.add_format()
    align_format_1.set_align('right')
    align_format_1.set_font_color('#0000FF')
    align_format_2.set_align('right')
    align_format_2.set_font_color('#008000')
    align_format_3.set_align('right')
    align_format_3.set_font_color('#FF0000')
    worksheet.set_column('A:A', 30)
    worksheet.write('A1', "Document Summary", bold)
    worksheet.write('A2', "Total Matches", italic)
    worksheet.write('B2', summary_data[0])
    worksheet.write('A3', "Total Countries", italic)
    worksheet.write('B3', summary_data[1])
    worksheet.write('A4', "Total Tournaments", italic)
    worksheet.write('B4', summary_data[2])
    worksheet.write('A5', "Total Goals Scored", italic)
    worksheet.write('B5', summary_data[3])
    worksheet.write('A6', "Average Goals Per Match", italic)
    worksheet.write('B6', np.longdouble(avg_g))
    worksheet.write('A8', "Country Summary", bold)
    worksheet.write('B8', "MP", align_format_1)
    worksheet.write('C8', "GF", align_format_2)
    worksheet.write('D8', "GA", align_format_3)

    worksheet.write('A9', g_data[0], italic)
    worksheet.write('B9', g_data[1], align_format_1)
    worksheet.write('C9', g_data[2], align_format_2)
    worksheet.write('D9', g_data[3], align_format_3)

    worksheet.write('A10', f_data[0], italic)
    worksheet.write('B10', f_data[1], align_format_1)
    worksheet.write('C10', f_data[2], align_format_2)
    worksheet.write('D10', f_data[3], align_format_3)

    worksheet.write('A11', s_data[0], italic)
    worksheet.write('B11', s_data[1], align_format_1)
    worksheet.write('C11', s_data[2], align_format_2)
    worksheet.write('D11', s_data[3], align_format_3)

    worksheet.write('A12', e_data[0], italic)
    worksheet.write('B12', e_data[1], align_format_1)
    worksheet.write('C12', e_data[2], align_format_2)
    worksheet.write('D12', e_data[3], align_format_3)

    worksheet.write('A13', n_data[0], italic)
    worksheet.write('B13', n_data[1], align_format_1)
    worksheet.write('C13', n_data[2], align_format_2)
    worksheet.write('D13', n_data[3], align_format_3)
    workbook.close()


def run():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', help='Football game scores from my birth to today')
    parser.add_argument("-f", help="Data File")
    parser.add_argument("-o", help="Output File")
    args = parser.parse_args()
    filename = args.f
    output = args.o
    check_file(filename)
    data = read_file(filename)
    if output is None:
        display(data)
    else:
        path = (r"/Users/berkecengiz/Desktop/LAB8/{}").format(output)
        save(data, path)

if __name__ == '__main__':
    run()
