import requests
import json
import pandas as pd
import numpy as np

def send_json(json_obj):
    api_url = "https://api-sandbox.clear.in/einv/v2/eInvoice/generate"
    headers = {
        'x-cleartax-auth-token': "1.09f0a25d-62c0-4195-9741-07a61926e61f_b56aee09e37bef57f28763f2f2ce2a5b5c106f6143ab36556fee9eada02791d0",
        'gstin': '05AAFCD5862R012',
        'Content-Type': 'application/json'}
    res = requests.put(api_url, data=json.dumps(json_obj), headers=headers)
    return res.json()


def create_item_object(df_items_each):
    items_list = []
    # iterate to get all the items
    for i in range(df_items_each.shape[0]):
        items_dict = {}
        items_dict["SlNo"] = int(df_items_each["ITEM_SERIAL_NUMBER"][i])
        items_dict["PrdDesc"] = df_items_each["ITEM_DESCRIPTION"][i]
        items_dict["IsServc"] = df_items_each["IS_SERVICE"][i]
        items_dict["HsnCd"] = df_items_each["HSN_CODE"][i]
        items_dict["Barcde"] = df_items_each["BARCODE"][i]
        items_dict["Qty"] = float(df_items_each["QUANTITY"][i])
        items_dict["FreeQty"] = float(df_items_each["FREE_QTY"][i])
        items_dict["Unit"] = df_items_each["UNIT_OF_MEASUREMENT"][i]
        items_dict["UnitPrice"] = float(df_items_each["ITEM_PRICE"][i])
        items_dict["TotAmt"] = float(df_items_each["GROSS_AMOUNT"][i])
        items_dict["Discount"] = float(df_items_each["ITEM_DISCOUNT_AMOUNT"][i])
        items_dict["PreTaxVal"] = float(df_items_each["PRE_TAX_VALUE"][i])
        # calculate AssAmount
        items_dict["AssAmt"] = float(df_items_each["GROSS_AMOUNT"][i] - df_items_each["ITEM_DISCOUNT_AMOUNT"][i])

        items_dict["GstRt"] = float(df_items_each["GST_RATE"][i])
        items_dict["IgstAmt"] = float(df_items_each["IGST_AMT"][i])
        items_dict["CgstAmt"] = float(df_items_each["CGST_AMT"][i])
        items_dict["SgstAmt"] = float(df_items_each["SGST_UTGST_AMT"][i])
        items_dict["CesRt"] = float(df_items_each["COMP_CESS_RATE_AD_VALOREM"][i])
        items_dict["CesAmt"] = float(df_items_each["COMP_CESS_AMT_AD_VALOREM"][i])
        items_dict["CesNonAdvlAmt"] = float(df_items_each["COMP_CESS_AMT_NON_AD_VALOREM"][i])
        items_dict["StateCesRt"] = float(df_items_each["STATE_CESS_RATE_AD_VALOREM"][i])
        items_dict["StateCesAmt"] = float(df_items_each["STATE_CESS_AMT_AD_VALOREM"][i])
        items_dict["StateCesNonAdvlAmt"] = float(df_items_each["STATE_CESS_AMT_NON_AD_VALOREM"][i])
        items_dict["OthChrg"] = float(df_items_each["OTHER_CHARGES_ITEM_LEVEL"][i])

        items_dict["TotItemVal"] = float(df_items_each["GROSS_AMOUNT"][i] - df_items_each["ITEM_DISCOUNT_AMOUNT"][i] + \
                                   df_items_each["IGST_AMT"][i] + \
                                   df_items_each["CGST_AMT"][i] + \
                                   df_items_each["SGST_UTGST_AMT"][i] + \
                                   df_items_each["COMP_CESS_AMT_AD_VALOREM"][i] + \
                                   df_items_each["COMP_CESS_AMT_NON_AD_VALOREM"][i] + \
                                   df_items_each["STATE_CESS_AMT_AD_VALOREM"][i] + \
                                   df_items_each["STATE_CESS_AMT_NON_AD_VALOREM"][i] + \
                                   df_items_each["OTHER_CHARGES_ITEM_LEVEL"][i])

        items_dict["OrdLineRef"] = float(df_items_each["PURCHASE_ORDER_LINE_REFERENCE"][i])
        items_dict["OrgCntry"] = df_items_each["ORIGIN_COUNTRY_CODE"][i]
        items_dict["PrdSlNo"] = df_items_each["UNIQUE_SERIAL_NUMBER"][i]
        items_dict["BchDtls"] = {}

        items_dict["BchDtls"]["Nm"] = df_items_each["BATCH_NUMBER"][i]
        items_dict["BchDtls"]["ExpDt"] = df_items_each["BATCH_EXPIRY_DATE"][i]
        items_dict["BchDtls"]["WrDt"] = df_items_each["WARRANTY_DATE"][i]
        # append to list
        items_list.append(items_dict)
    return items_list


def create_doc_details_object(df_invoice_each):
    doc_details = {}
    doc_details["Typ"] = df_invoice_each["DOCUMENT_TYPE_CODE"][0]
    doc_details["No"] = df_invoice_each["DOCUMENT_NUMBER"][0]
    doc_details["Dt"] = df_invoice_each["DOCUMENT_DATE"][0]
    return  doc_details

def create_transaction_object(df_invoice_each):
    tran_dict = {}
    print(df_invoice_each.info())
    tran_dict["Version"] = df_invoice_each["VERSION_NUMBER"][0]
    tran_dict["TranDtls"] = {}
    tran_dict["TranDtls"]["TaxSch"] = "GST"
    tran_dict["TranDtls"]["SupTyp"] = df_invoice_each["SUPPLY_TYPE_CODE"][0]

    return tran_dict

def create_valdtls_object():
    val_dtls_dict={}
    #write code here

    return val_dtls_dict

def create_seller_details_object(df_invoice_each):
    seller_dict={}

    return seller_dict

def create_buyer_details_object(df_invoice_each):
    buyer_dict={}

    return buyer_dict

def create_objects(df_invoice, df_items):
    final_list = []
    for i in range(df_invoice.shape[0]):
        if i>5:
            break
        row_dict = {}
        doc_number = df_invoice['DOCUMENT_NUMBER'][i]
        doc_id = df_invoice['DOCUMENT_ID'][i]
        # extracting all items for document_id
        df_items_each = df_items[df_items['DOCUMENT_ID'] == doc_id]
        df_items_each = df_items_each.sort_values('ITEM_SERIAL_NUMBER')  # sorting the serial number so that we get items in proper order
        df_items_each.reset_index(inplace=True, drop=True)

        df_invoice_each = df_invoice[df_invoice['DOCUMENT_ID'] == doc_id]
        df_invoice_each.reset_index(inplace=True, drop=True)

        row_dict["transaction"]=create_transaction_object(df_invoice_each)
        row_dict["DocDtls"] = create_doc_details_object(df_invoice_each)
        row_dict["SellerDtls"]= create_seller_details_object(df_invoice_each)
        row_dict["BuyerDtls"]= create_buyer_details_object(df_invoice_each)
        row_dict["ItemList"] = create_item_object(df_items_each)
        row_dict["ValDtls"] = create_valdtls_object()

        # appending all dictionary to final list i.e. JSON
        final_list.append(row_dict)
    return final_list


def run():
    f1 = open("invoice.json", "r")
    invoice_json_obj = json.load(f1)
    df_invoice = pd.DataFrame(invoice_json_obj)
    # print(df_invoice)
    items_file = open("items.json", "r")
    items_json_obj = json.load(items_file)
    df_items = pd.DataFrame(items_json_obj)

    final_json_array = create_objects(df_invoice, df_items)



    print(final_json_array)
    #creating json
    json_obj = json.dumps(final_json_array, indent=4)
    with open("final_schema.json", "w") as outfile:
        outfile.write(json_obj)

run()
