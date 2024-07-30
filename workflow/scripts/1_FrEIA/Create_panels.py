#!/usr/bin/env python3
# Author: Norbert Moldován
# Mouliere Lab
# Amsterdam UMC
# Vrije Universiteit Amsterdam


# The script creates a panel of controls and a panel of cases
# from trinucleotide proportion data.
# These can be used as preset median vectors from which
# the Euclidean distances are measured when calculating the FrEIA score.

import argparse
import pandas as pd

def argumentparsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_trinucleotide",
                        dest="in_tnc",
                        type=str,
                        help="The path to the file containing the fragment end trinucleotide proportions "
                             "for controls and cancer from the results sub-folder .../4_FrEIA/4_Compare/Data. "
                             " Files must be a .csv file!",
                        default="Dat_GT__sample.csv")
    parser.add_argument("--input_diversity",
                        dest="in_div",
                        type=str,
                        help="The path to the file containing the fragment end diversity"
                             "for controls and cancer from the results sub-folder .../4_FrEIA/4_Compare/Data. "
                             "Files must be a .csv file!",
                        default="Dat_GT__MDS_sample.csv")

    parser.add_argument("--input_trinucleotide_controls",
                        dest="in_tnc_ctr",
                        type=str,
                        help="The path to the file containing the fragment end trinucleotide proportions "
                             "for controls. Files must be a .csv file!")
    parser.add_argument("--input_diversity_controls",
                        dest="in_div_ctr",
                        type=str,
                        help="The path to the file containing the fragment end diversity"
                             "for controls. Files must be a .csv file!")
    parser.add_argument("--input_trinucleotide_cases",
                        dest="in_tnc_cas",
                        type=str,
                        help="The path to the file containing the fragment end trinucleotide proportions "
                             "for cases. Files must be a .csv file!")
    parser.add_argument("--input_diversity_cases",
                        dest="in_div_cas",
                        type=str,
                        help="The path to the file containing the fragment end diversity"
                             "for cases. Files must be a .csv file!")
    parser.add_argument("-o", "--output",
                        dest="outpath",
                        type=str,
                        required=True,
                        help="The path to the output file.")
    return parser.parse_args()


def median_vector(dat_Df):
    median_Df = dat_Df.median().reset_index()

    return median_Df

def main():
    args = argumentparsing()  # Parse arguments.

    try:
        tnc_Df = pd.read_csv(args.in_tnc,
                             sep=",")  # Read all samples trinucleotide proportions.
        div_Df = pd.read_csv(args.in_div,
                             sep=",")  # Read all samples diversity.

        tnc_ctr_Df = tnc_Df[tnc_Df['WhichGroup'] == 'control'].rename(columns={"WhichSample": "sample_name",
                                                                               "WhichGroup": "group"})
        tnc_cas_Df = tnc_Df[tnc_Df['WhichGroup'] == 'cancer'].rename(columns={"WhichSample": "sample_name",
                                                                              "WhichGroup": "group"})

        div_ctr_Df = div_Df[div_Df['group'] == 'control']
        div_cas_Df = div_Df[div_Df['group'] == 'cancer']

    except OSError:
        tnc_ctr_Df = pd.read_csv(args.in_tnc_ctr,
                                 sep=",")  # Read control trinucleotide proportions.
        div_ctr_Df = pd.read_csv(args.in_div_ctr,
                                 sep=",")  # Read control diversity.
        tnc_cas_Df = pd.read_csv(args.in_tnc_cas,
                                 sep=",")  # Read case trinucleotide proportions.
        div_cas_Df = pd.read_csv(args.in_div_cas,
                                 sep=",")  # Read case diversity.

    # Merge trinucleotides with diversity.
    ctr_Df = tnc_ctr_Df.merge(div_ctr_Df)
    cas_Df = tnc_cas_Df.merge(div_cas_Df)

    # Compute median vector.
    median_ctr_Df = pd.DataFrame({"ctr": pd.Series(ctr_Df.median(numeric_only=True))}).reset_index()
    median_cas_Df = pd.DataFrame({"case": pd.Series(cas_Df.median(numeric_only=True))}).reset_index()

    # Create and save output.
    out_Df = median_ctr_Df.merge(median_cas_Df)
    out_Df.rename(columns={"index": "base"},
                  inplace=True)
    out_Df.to_csv(args.outpath,
                  index=False)
    print("\nThe file containing panel of medians is available at:",
          args.outpath)

if __name__ == "__main__":
    main()