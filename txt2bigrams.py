import pandas as pd
import sys
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
import csv
import os
import string
file_name = sys.argv[1]
txts_folder = sys.argv[2]


def main():
	df = pd.read_csv(file_name, encoding='utf-8-sig')
	os.mkdir(file_name+"_bigrams")

	filenames_list = []
	sentiment_list = []
	for idx, row in df.iterrows():
		txt_file_name = df.loc[idx, "file_name_complete"]

		with open(txts_folder+"/"+txt_file_name, 'r') as currentfile:
			review_text = currentfile.read().replace('\n', '')
			review_text = review_text.translate(str.maketrans('','',string.punctuation))
			review_tokens = nltk.word_tokenize(review_text)
			token_count = 0
			for token in review_tokens:
				review_tokens[token_count] = token.lower()
				token_count += 1
			review_tokens = [token for token in review_tokens if (not token in stopwords.words('english')) and len(token) >= 2]
			bigrams = nltk.FreqDist(ngrams(review_tokens, 2))

			bigram_filename = txt_file_name[:-9]+"_bigrams.csv"
			filenames_list.append(bigram_filename)
			
			with open(file_name+"_bigrams/"+bigram_filename, "w") as outfile:
				writer = csv.writer(outfile)
				writer.writerow(["BIGRAM", "COUNT"])
				for bigram in bigrams.most_common():
					writer.writerow([" ".join(bigram[0]), bigram[1]])

	df["bigram_file_name"] = filenames_list
	df.to_csv(file_name+"BIGRAM_REF.csv",index=False)


if __name__ == "__main__": main()