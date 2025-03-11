import pandas as pd

def compare_files(file1_path, file2_path):
    # Read both files
    invoice_df = pd.read_csv(file1_path)
    award_df = pd.read_csv(file2_path)

    # Comparison 1: Total records
    total_invoice = len(invoice_df)
    total_award = len(award_df)
    comparison1 = {
        "File1_Total_Records": total_invoice,
        "File2_Total_Records": total_award,
        "Match": total_invoice == total_award
    }

    # Comparison 2: Transaction Type 1 records
    tt1_invoice = invoice_df[invoice_df['transaction_type'] == 1]
    tt1_award = award_df[award_df['transaction_type'] == 1]
    comparison2 = {
        "File1_TT1_Records": len(tt1_invoice),
        "File2_TT1_Records": len(tt1_award),
        "Match": len(tt1_invoice) == len(tt1_award)
    }

    # Comparison 3: Check if "Not Funded" has covers_adjustment=1
    # Assuming "Not Funded" is in fp_status column
    not_funded_award = award_df[award_df['fp_status'] == "Not Funded"]
    check_adjustment = not_funded_award['covers_adjustment'].eq(1).all()
    comparison3 = {
        "Not_Funded_Records": len(not_funded_award),
        "All_Cover_Adjustment_1": check_adjustment
    }

    # Comparison 4: Sum of disbursed status for TT1
    # Assuming "disbursed" is a status in fp_status and amount is "factoring_amount"
    disbursed_award = award_df[(award_df['transaction_type'] == 1)
                               & (award_df['fp_status'] == "disbursed")]
    sum_award = disbursed_award['factoring_amount'].sum()
    # For Invoice file, assuming similar logic (adjust column names if needed)
    disbursed_invoice = invoice_df[(invoice_df['transaction_type'] == 1)
                                   & (invoice_df['fp_status'] == "disbursed")]
    sum_invoice = disbursed_invoice['discounted_invoice_amount'].sum()
    comparison4 = {
        "File1_Disbursed_Sum": sum_invoice,
        "File2_Disbursed_Sum": sum_award,
        "Match": sum_invoice == sum_award
    }

    # Comparison 5: Count repaid status in Award file
    repaid_count = len(award_df[award_df['fp_status'] == "repaid"])
    comparison5 = {"Repaid_Records_in_Award": repaid_count}

    return {
        "Total_Records_Comparison": comparison1,
        "Transaction_Type_1_Comparison": comparison2,
        "Not_Funded_Adjustment_Check": comparison3,
        "Disbursed_Sum_Comparison": comparison4,
        "Repaid_Records_in_Award": comparison5
    }


# Example usage
result = compare_files("invoice.csv",
                       "aditya_birla_treds_rfd_award_2025-03-11.csv")
print(result)
