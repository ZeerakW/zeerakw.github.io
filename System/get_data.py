#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, json, networkx, nltk, os, codecs

# Issues and candidates http://www.ontheissues.org/Grid_Frontrunners.htm

#### McCains 
# Top Contributors: http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00006424
# Contributions by industry: http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00006424

#### Ron Paul
# Top Contributors: http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00005906
# Contirubitions by industry: http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00005906

#### Obama
# Top Contributors: http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00009638
# Contributors by industry: http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00009638

def download(site, out):
    """
    :param site: url to download
    :param out: file to save to
    """


    return 0

def get_orgs(in_file, out_file):

    f_out = io.open(out_file, 'w', encoding = 'utf-8')
    f_out.write('Organisation\tOrg Id\tContribution\n')
    org_contrib = []

    for line in io.open(in_file, 'r', encoding = 'utf-8'):
        if '"/orgs/summary.php?' in line:
            org = line.split('>')[1].split('<')[0].rstrip()
            org_id = line.split('=')[2].split('"')[0]
            f_out.write(org + '\t' + org_id + '\t')
        elif '<td class="number">' in line:
            num = line.split('>').split('<')[0]
            f_out.write(num + '\n')
        else:
            continue

        org_contrib.append((org, org_id, num))

    f_out.close()

    return 1

def get_inds(in_file, out_file):

    f_out = io.open(out_file, 'w', encoding = 'utf-8')
    f_out.write('Industry\tContribution\n')

    ind_contrib = []

    industries = False
    for line in io.open(in_file, 'r', encoding = 'utf-8'):
        if 'id="industries"' in line:
            industries = True

        if industries:
            if '<td nowrap>' in line:
                industry = line.split('>')[1].split('<')[0]
                f_out.write(industry + '\t')

            if '<td class="number"' in line:
                contrib = line.split('>')[1].split('<')[0]
                f_out.write(contrib)

            if '</tbody>'' in line and industries:
                industries = False
                break

    f_out.close()

    return 2

def get_org_issue_hist(in_file, out_file):

    f_out = io.open(out_file, 'w', encoding = 'utf-8')
    f_out.write('Issue\tNumber of Issues\tNumber of reports\n')
    org_issues = []

    issues = False
    for line in io.open(in_file, 'r', encoding = 'utf-8'):
        if 'id="client-issues"' in line:
            issues = True

        if issues:
            if '<a href=' in line:
                issue = line.split('>')[1].split('<')[0]
                f_out.write(issue + '\t')

            if '<td class="center">' == line:
                no_of_issues = line.split('>')[1].split('<')[0]
                f_out.write(no_issues + '\t')

            if '<td class="center">' in line and '</td>' in line:
                no_of_reports = line.split('>')[1].split('<')[0]
                f_out.write(no_of_reports + '\n')

            if '</tbody>' in line:
                issues = False
                break
    f_out.close()
    return 0


def main():
    # TODO Get organisation interests
    # TODO Get politicians standings on issues (through links on grid)

    ## Download politician info
    rawdir = os.getcwd() + '/data/raw/'
    outdir = os,getcwd() + '/data/cleaned/'

    # Download McCain info
    download('http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00006424', rawdir + 'mccain_top')
    download('http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00006424'  , rawdir + 'mccain_ind')

    # Download Ron Paul info
    download('http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00005906', rawdir + 'paul_top')
    download('http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00005906'  , rawdir + 'paul_ind')

    # Download Obama info
    download('http://www.opensecrets.org/pres08/contrib.php?cycle=2008&cid=N00009638', rawdir + 'obama_top')
    download('http://www.opensecrets.org/pres08/indus.php?cycle=2008&cid=N00009638'  , rawdir + 'obama_ind')

    ## Clean Politician info
    # McCain
    get_inds(rawdir + 'mccain_ind', outdir + 'mccain_ind_clean')
    get_orgs(rawdir + 'mccain_top', outdir + 'mccain_top_clean')

    # Paul
    get_inds(rawdir + 'paul_ind', outdir + 'paul_ind_clean')
    get_orgs(rawdir + 'paul_top', outdir + 'paul_top_clean')

    # Obama
    get_inds(rawdir + 'obama_ind', outdir + 'obama_ind_clean')
    get_orgs(rawdir + 'obama_top', outdir + 'obama_top_clean')
