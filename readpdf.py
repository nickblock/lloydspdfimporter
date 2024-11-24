from pypdf import PdfReader
import csv
import decimal

months = [
  "january",
  "febuary",
  "march",
  "april",
  "may",
  "june",
  "july",
  "august",
  "september",
  "october",
  "november",
  "december"
]


class LloydsPdfImporter:

  transactions = []

  def process_line(self, line: str):

    split = line.split(' ')

    if(len(split) > 5):

      try:

        if not str(split[1]).lower() in months:
          return False
        
        if not str(split[3]).lower() in months:
          return False
        


        number_one = int(split[0])
        number_two = int(split[2])

        value_idx = len(split)-1

        credit = False

        if(split[-1] == "CR"):
          value_idx = len(split)-2
          credit = True

        date = " ".join([split[0], split[1]])

        text = " ".join(split[5:value_idx])

        value = float(split[value_idx].replace(',', ''))

        if credit:
          credit = "CR"
        else: 
          credit = ""

        transaction = [date, text, value, credit]

        self.transactions.append(transaction)
        
        return True


      except ValueError as err:
        print(err)
        return False
      
      
    else:
      return False

  def process_file(self, file_name: str):

    reader = PdfReader(file_name)

    for page in reader.pages:
      text = page.extract_text()
      for line in text.split("\n"):
        if self.process_line(line):
          print(line)

  def export_csv(self, csv_file: str):

    with open(csv_file, 'w') as csv_out:
      csv_writer = csv.writer(csv_out, delimiter=',')

      for trans in self.transactions:
        csv_writer.writerow(trans)
  
statements = [
"/home/nick/Downloads/Statement_6862_Jan-24.pdf",
"/home/nick/Downloads/Statement_6862_Feb-24.pdf",
"/home/nick/Downloads/Statement_6862_Mar-24.pdf",
"/home/nick/Downloads/Statement_6862_Apr-24.pdf",
"/home/nick/Downloads/Statement_6862_May-24.pdf",
"/home/nick/Downloads/Statement_6862_Jun-24.pdf",
"/home/nick/Downloads/Statement_6862_Jul-24.pdf",
"/home/nick/Downloads/Statement_6862_Aug-24.pdf",
"/home/nick/Downloads/Statement_6862_Sep-24.pdf",
"/home/nick/Downloads/Statement_6862_Oct-24.pdf",
"/home/nick/Downloads/Statement_6862_Nov-24.pdf"]

lloydsImporter = LloydsPdfImporter()

for statement in statements:

  lloydsImporter.process_file(statement)

lloydsImporter.export_csv("/home/nick/Downloads/lloyds.csv")

