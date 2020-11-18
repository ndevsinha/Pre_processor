import random
import pandas as pd
from nltk.corpus import stopwords
import nltk.stem
from Stemmer import Stemmer
import nltk
from string import punctuation
import json
from itertools import chain, starmap
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
class Preprocessor:
    #intializing the parameters with instance creation
    def __init__(self,file,filetype=None):
        flag=0
        if isinstance(file,str):
            if "csv" in file.split("."):
                file1 = pd.read_csv(file, encoding="ISO-8859-1")
                flag=1
            if "json" in file.split("."):
                with open(file) as f:
                    file1=json.load(f)
                flag=1
                    
        if filetype is None:
            if isinstance(file,pd.DataFrame):
                filetype = "dataframe"
            elif isinstance(file,dict):
                filetype = "json"
        elif filetype in ["dataframe","json"]:
            filetype = filetype

        else:
            raise Exception("Filetyp should be either dataframe or json")
        self.filetype = filetype
        if flag==1:
            self.df = file1
        else:
            self.df = file
        
    
    def df_preprocessor(self,threshold_4_delete_null=None,no_null_columns=None,numeric_null_replace=None,textual_column_word_tokenize=False,textual_column_word_normalize=False):
        
        self.threshold_4_delete_null = threshold_4_delete_null
        self.no_null_columns = no_null_columns
        self.numeric_null_replace = numeric_null_replace
        self.textual_column_word_tokenize = textual_column_word_tokenize
        self.textual_column_word_normalize = textual_column_word_normalize
        
        #Record initial columns as input        
        init_columns = list(self.df.columns)
        
        #Delete columns having more than default 50% null values
        if self.threshold_4_delete_null is None:
            self.threshold_4_delete_null=0.5
        self.df = self.df.loc[:, self.df.isin([' ','NULL',None,""]).mean() < self.threshold_4_delete_null]
        deleted_null_columns = set(init_columns) - set(list(self.df.columns))
        if len(deleted_null_columns)>0:
            print("Columns having more than 50% null values have been deleted. Deleted Columns are : ",deleted_null_columns)
        
        #Finding numeric and non-numeric columns
        numeric_columns = list(self.df.select_dtypes(include=numerics).columns)
        non_numeric_columns = list(set(init_columns) - set(numeric_columns))
        
        if self.no_null_columns is not None:
            if isinstance(self.no_null_columns,list):
                for i in self.no_null_columns:
                    self.df = self.df.dropna(axis=0, subset=[i])
            else:
                raise Exception("no_null_columns must be of type list")
                
        #finding textual columns if exists
        textual_columns = []        
        for i in non_numeric_columns:
            if self.df[i].dtype==object:
                
                x=self.df.iloc[random.randint(0,len(self.df))][i]
                y=self.df.iloc[random.randint(0,len(self.df))][i]
                if type(x)!=str or type(y)!=str:
                    continue
                space_in_x = len([k for k,letter in enumerate(x) if letter==" "])
                space_in_y = len([k for k,letter in enumerate(y) if letter==" "])
                if space_in_x>=1 or space_in_y>=1:
                    textual_columns.append(i)
        #handling missing values in numeric columns
        for col in numeric_columns:
            self.df[col].fillna((self.df[col].mean()), inplace=True)
        
        #handling missing values in categorical columns
        for col in list(set(non_numeric_columns)-set(textual_columns)):
            self.df[col]=self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        #handling textual columns using text preprocessing
        stop_words = set(stopwords.words('english'))
        if len(textual_columns)>0:
            for col in textual_columns :
                self.df[col]=self.df[col].astype(str)
                self.df[col]=self.df[col].apply(lambda x: ''.join([x.lower()]))
                self.df[col] = self.df[col].apply(lambda x: ''.join(c for c in x if c not in punctuation))
                self.df[col] = self.df[col].str.replace(' \d+', '')
                self.df[col] = self.df[col].str.replace(r"http\S+", '')
                self.df[col] = self.df[col].str.replace(r"www\S+", '')
                self.df[col] = self.df[col].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
                
                if self.textual_column_word_tokenize==True:
                    self.df[col] = self.df[col].apply(nltk.word_tokenize)
                    if self.textual_column_word_normalize is not None:
                        if self.textual_column_word_normalize=="porter":
                            stemmer = Stemmer('porter').stemmer
                        elif self.textual_column_word_normalize=="snowball":
                            stemmer = Stemmer('snowball').stemmer
                        elif self.textual_column_word_normalize=="lemmatize":
                            stemmer = Stemmer('lemmatize').stemmer
                        else :
                            raise Exception("parameter textual_column_word_normalize is not valid option")
                        self.df[col]=self.df[col].apply(lambda x: ' '.join([stemmer.stem(w,'v') for w in x]))
                        
        
     
        return self.df
    
    
    
    
    def json_preprocessor(self):

        self.dictionary = self.df
        def unpack(prev_key, prev_value):
            """Unpack one level of nesting in json file"""
            # Unpack one level only!!!

            if isinstance(prev_value, dict):
                for key, value in prev_value.items():
                    temp1 = prev_key + '_' + key
                    yield temp1, value
            elif isinstance(prev_value, list):
                i = 0 
                for value in prev_value:
                    temp2 = prev_key + '_'+str(i) 
                    i += 1
                    yield temp2, value
            else:
                yield prev_key, prev_value    


        # Keep iterating until the termination condition is satisfied
        while True:
            # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
            self.dictionary = dict(chain.from_iterable(starmap(unpack, self.dictionary.items())))
            # Terminate condition: not any value in the json file is dictionary or list
            if not any(isinstance(value, dict) for value in self.dictionary.values()) and \
               not any(isinstance(value, list) for value in self.dictionary.values()):
                break

        return self.dictionary
