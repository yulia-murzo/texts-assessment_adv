import inflection
import glob
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv



class term_analysis:
    def __init__(self, term_name, term_number):
        self.term_name = term_name
        self.term_number = term_number

nltk.download('stopwords')
nltk.download('punkt')


def get_texts_statistic(route):
    dir_files = glob.glob(route)
    dir_files.sort()

    # RDF/XML header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\nxmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\nxmlns:foaf='http://xmlns.com/foaf/0.1/'\n>")

    f_rdf = open("training_texts_data.xml", "wt", encoding="utf-8")
    f_rdf.write(header)
    j = 1
    for file in dir_files:
        try:
            with open(file, encoding='utf-8') as f:
                #Reading the file data
                s = f.read()
                #Text pre=procrssing
                s = s.replace('"', '')  #Delete "
                s = s.replace("'", "")  # Delete '
                s = s.replace('.', '')  #Delete .
                s = s.replace('?', '')  #Delete ?
                s = s.replace(',', '')  #Delete ,
                s = s.replace('\n', ' ')    #Delete \n
                s = re.sub(" +", " ", s)    #Delete multiple spaces
                s = s.lower()  # To lower case
                # Text to list
                tokens = word_tokenize(s)
                p = [word for word in tokens if not word in stopwords.words('english')]
                #To singular
                for i in range(len(p)):
                    p[i] = inflection.singularize(p[i])
        except IsADirectoryError:
            print('A Directory has been found. Move to the next file: ', file)
            continue
        except PermissionError:
            print('Permission Error: ', file)
            continue

        report = []

        #Calculate term frequency
        total_terms = len(p)
        for item in p:
            if len(item) > 2:
                item_count = p.count(item)
                report.append(term_analysis(item, item_count))
                #Remove the term from the list
                flag = True
                while flag:
                    try:
                        p.remove(item)
                    except ValueError:
                        flag = False
        #Write entry about training text to RDF/XML file
        f_rdf.write("\n<!--Training text definition-->\n<rdf:Description rdf:about='http://127.0.0.1/" + file + "/'>\n<my:has_id>" + file + "</my:has_id>\n<my:TotalTerms rdf:datatype='http://www.w3.org/2001/XMLSchema#int'>" + str(total_terms) + "</my:TotalTerms>\n</rdf:Description>")
        for item in report:
            print(item.term_name, item.term_number, j)
            f_rdf.write(
                "\n<!--Term entry definition-->\n<rdf:Description rdf:about='http://127.0.0.1/" + str(item.term_name) + "_" + str(j) + "/'>\n<rdfs:label>" + str(item.term_name) + "</rdfs:label>\n<my:EntriesNumber rdf:datatype='http://www.w3.org/2001/XMLSchema#int'>" + str(item.term_number) + "</my:EntriesNumber>\n<foaf:member><rdf:Description rdf:about='http://127.0.0.1/" + file + "/' /></foaf:member>\n</rdf:Description>")
            j = j + 1
    f_rdf.write("\n</rdf:RDF>\n")
    f_rdf.close()
    return True

def get_minimums(route):
    dir_files = glob.glob(route)
    dir_files.sort()

    # RDF/XML header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\nxmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\nxmlns:foaf='http://xmlns.com/foaf/0.1/'\n>")

    f_rdf = open("minimums_data.xml", "wt", encoding="utf-8")
    f_rdf.write(header)
    j = 1
    for file in dir_files:
        print('file=',file)
        try:
            with open(file, encoding="utf-8") as fconf_obj:
                reader = csv.DictReader(fconf_obj, delimiter=';')
                print('reader=',reader)
                report = []
                for line in reader:
                    report.append(line["WORD"].lower())
            print('report=',report)
        except IsADirectoryError:
            print('A Directory has been found. Move to the next file: ', file)
            continue
        except PermissionError:
            print('Permission Error: ', file)
            continue

        #Write entry about training text to RDF/XML file
        total_terms = len(report)
        f_rdf.write("\n<!--Lexical minimum definition-->\n<rdf:Description rdf:about='http://127.0.0.1/" + file + "/'>\n<my:has_id>" + file + "</my:has_id>\n<rdf:type>DomainTemplate</rdf:type>\n<my:TotalTerms rdf:datatype='http://www.w3.org/2001/XMLSchema#int'>" + str(total_terms) + "</my:TotalTerms>\n</rdf:Description>")
        for item in report:
            print(item, j)
            f_rdf.write(
                "\n<!--Lexical minimum entry definition-->\n<rdf:Description rdf:about='http://127.0.0.1/" + str(item.replace("'","")) + "_" + str(j) + "/'>\n<rdfs:label>" + str(item.replace("'","")) + "</rdfs:label>\n<foaf:member><rdf:Description rdf:about='http://127.0.0.1/" + file + "/' /></foaf:member>\n</rdf:Description>")
            j = j + 1
    f_rdf.write("\n</rdf:RDF>\n")
    f_rdf.close()
    return True





route = 'texts/*.txt'
get_texts_statistic(route)
route = 'minimums/*.csv'
get_minimums(route)