# -*- coding: utf-8 -*-
import os

from transformers import BertConfig, BertTokenizer, BertModel

import torch
import torch.nn as nn

from .utils import *


class SentimentModel(nn.Module):

    def __init__(self, config):
        super(SentimentModel, self).__init__()

        data_path = f'{os.path.dirname(os.path.abspath(__file__))}/data'
        config_path = f'{data_path}/model/config.json'
        # model_path = f'{data_path}/model/epoch=3__f1=0.741.pt'

        self.config = BertConfig.from_pretrained(config_path)

        self.bert = BertModel(self.config)

        # self.dropout = nn.Dropout(self.config.hidden_dropout_prob)
        self.nn = nn.Linear(self.config.hidden_size, 3)

    def forward(self, input_ids, attention_mask, token_type_ids):
        pooled_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids)[1]

        # pooled_output = self.dropout(pooled_output)
        logits = self.nn(pooled_output)

        return logits

class SentimentDetection():

    def __init__(self, gpu=False):

        data_path = f'{os.path.dirname(os.path.abspath(__file__))}/data'

        self.tokenizer = BertTokenizer.from_pretrained(f'{data_path}/pars_bert_tokenizer')

        config = BertConfig.from_pretrained(f'{data_path}/model/config.json')

        self.model = SentimentModel(config)

        self.gpu = gpu
        self.device = 'cpu'
        if self.gpu:
            self.model = self.model.cuda()
            self.device = 'cuda:0'

        self.model_path = f'{data_path}/model/pytorch_model.bin'
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.eval()

    def infer(self, data):
        data['label'] = -1
        data['clean_text'] = data['text'].apply(lambda text: preprocessor(text))

        input_data = list(data['clean_text'])

        tokenized_data = self.tokenizer.batch_encode_plus(input_data,
                                                          add_special_tokens=True,
                                                          truncation=True,
                                                          max_length=256,
                                                          return_token_type_ids=True,
                                                          padding='max_length',
                                                          return_attention_mask=True,
                                                          return_tensors='pt')


        input_ids = tokenized_data['input_ids']
        attention_mask = tokenized_data['attention_mask']
        token_type_ids = tokenized_data['token_type_ids']

        # move tensors to GPU if CUDA is available
        if self.gpu:
            input_ids = input_ids.to(self.device)
            attention_mask = attention_mask.to(self.device)
            token_type_ids = token_type_ids.to(self.device)

        with torch.no_grad():
            # compute predicted outputs by passing inputs to the model
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids
                )

        _, preds = torch.max(outputs, dim=1)

        data['output'] = preds.cpu()

        data['label'] = data['output'].replace(0, 'منفی').replace(1, 'خنثی').replace(2, 'مثبت')

        data = data.drop(['clean_text', 'output'], axis=1)

        return data
