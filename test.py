import nltk
nltk.download("punkt")
nltk.download("stopwords")
from rake_nltk import Rake
import pandas as pd
import xlsxwriter

def extract_keywords(i):
    export = pd.read_excel(f'keywords.xlsx', header=None)
    keyword_list = export.values.T[0].tolist()
    # workbook = xlsxwriter.Workbook(f'_keyword.xlsx')
    # worksheet = workbook.add_worksheet()
    final_keyword_list2 = []

    for cell in keyword_list:
        try:
            r = Rake()
            r.extract_keywords_from_text(cell)
            final_keyword_list1 = ""
            for rating, keyword in r.get_ranked_phrases_with_scores():
                if rating >= 15:

                    final_keyword_list1 += keyword + " , "

                    # final_keyword_list1.append(keyword + " ^ ")
                    # for word in final_keyword_list1:
                    #     word += "\n"
            final_keyword_list2.append(final_keyword_list1)
        except:
            final_keyword_list2.append(" ")
    return final_keyword_list2[i]
    # for row_index, element in enumerate(final_keyword_list2, start=0):
    #     worksheet.write(row_index, 0, element)

    # print(final_keyword_list2)

    # workbook.close()