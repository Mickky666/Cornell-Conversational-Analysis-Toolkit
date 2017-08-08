import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
class CountUtterance:
    """
    This class takes corpus as input and count the utturances features,
    Argument:
    corpus:A processed text data loaded from json file
        for more detail see convokit/model.py
    Features:
    1. Utterance Count
    2. Directed Pairs

    Compatible with subdivided users.
    """

    #load the corpus, count the utterance and store them in self.count_list
    def __init__(self,corpus,sort = True,sub_divide_user = False):
        self.corpus = corpus
        self.count_dict = {}
        for u in corpus.utterances.values():
            user = u.user
            rep = user.__rep__()
            if sub_divide_user:
                userid = rep['name']+' with ' + str(rep['attribs'])[1:-1]
            else:
                userid = rep['name']
            if user in corpus.users():
                self.count_dict.setdefault(userid,0)
                self.count_dict[userid] += 1
        self.count_list = sorted(self.count_dict.items(),key = lambda x:x[1])[::-1]

    #print the count result from self.count_list
    #print amount limited by argument number_to_print
    def print_count(self,number_to_print = None):
        if number_to_print == None:
            for uttercount in self.count_list:
                print(uttercount[0] + ' : ' + str(uttercount[1]))
        else:
            for i in range(number_to_print):
                uttercount = self.count_list[i]
                print(uttercount[0] + ' : ' + str(uttercount[1]))

    #return a dictionary containing userid as keys and number of utterances as values
    def __list__(self):
        return self.count_list

    #return a list containing lists of userid and number of utterances
    def __dict__(self):
        return self.count_dict
    
    
    """
    This method "directed_pairs" is used to compute the number of the directed pair between two different users.
    It returns the number of pairs or a list contain all the reply from User_A to User_B.
    Argument:
    User_A:User Object, see more detail in model.py
    User_B:Another User Object, see more detail in model.py
    sub_divide_user:If False, User's name will be used to count directed pairs.
        Otherwise, User ID will be used to count directed pairs.
    print_utterance: If True, the matched utterances pair will be printed.
    return_text: If True, the method will return a list containing all the utterance.
    """
    def directed_pairs(self,User_A,User_B,sub_divide_user = False,print_utterance = False,return_text = False):
        count_number = 0
        directed_pairs_list = []
        key_set = set(self.corpus.utterances.keys())
        if not sub_divide_user:
            for u in self.corpus.utterances.values():
                if u.reply_to not in key_set:
                    continue
                else:
                    if u.user._get_name() == User_A._get_name() and \
                    self.corpus.utterances[u.reply_to].user._get_name() == User_B._get_name():
                        count_number += 1
                        directed_pairs_list.append(u.text)
        else:
            for u in self.corpus.utterances.values():
                if u.reply_to not in key_set:
                    continue
                else:
                    if u.user.__repr__() == User_A.__repr__() and \
                    self.corpus.utterances[u.reply_to].user.__repr__() == User_B.__repr__():
                        count_number += 1
                        directed_pairs_list.append(u.text)
        if print_utterance:
            print('Following is the directed reply from ' + User_A._get_name() +' TO ' + \
                  User_B._get_name())
            if sub_divide_user == 0:
                print('Subdivide User is On!')
                print(User_A.__rep__()['name'] + ' with ' + str(User_A.__rep__()['attribs'])[1:-1])
                print(User_B.__rep__()['name'] + ' with ' + str(User_B.__rep__()['attribs'])[1:-1])
            print('='*50)
            for reply in directed_pairs_list:
                print(reply)
            print('='*50)
            print('Totally ' + str(count_number) + 'directed pairs.')
        if return_text:
            return directed_pairs_list
        else:
            return count_number
    """
    This methods pairs_feature is used to count all the directed utterance pairs among all the users in the text corpus.
    It takes only one argument: sub_divide_user. If it's True, then the user's userid will be used as identification.
    Otherwise, user's name will be used.

    It returns nothing but it will store the directed pairs in the self.asym_feature_list
    """
    
    def pairs_feature(self,sub_divide_user = False):
        pair_dict = {}
        key_set = set(self.corpus.utterances.keys())
        for u in self.corpus.utterances.values():
            if u.reply_to not in key_set:
                continue
            else:
                if sub_divide_user:
                    rep1 = u.user.__rep__()
                    rep2 = self.corpus.utterances[u.reply_to].user.__rep__()
                    key = '|' + rep1['names'] + ' with ' + str(rep1['attribs'])[1:-1] + '|' + ' Reply To ' +'|' \
                    + rep2['names'] + ' with ' + str(rep2['attribs'])[1:-1] + '|'
                    pair_dict.setdefault(key,0)
                    pair_dict[key] += 1
                else:
                    name1 = u.user._get_name()
                    name2 = self.corpus.utterances[u.reply_to].user._get_name()
                    key = '|' + name1 + '|' + ' Reply To ' + '|' + name2 + '|'
                    pair_dict.setdefault(key,0)
                    pair_dict[key] += 1

        feature_dict = {}
        dup_key_set = set()
        for key,value in pair_dict.items():
            inverse_key = ' Reply To '.join(key.split(' Reply To ')[::-1])
            if inverse_key in pair_dict.keys() and inverse_key not in dup_key_set:
                inverse_value = pair_dict[inverse_key]
                feature_dict[' & '.join(key.split(' Reply To '))] = (value+inverse_value,abs(value - inverse_value))
                dup_key_set.add(key)
                dup_key_set.add(inverse_key)
            else:
                feature_dict[key] = (value,value)
        feature_list = sorted(feature_dict.items(),key = lambda x:x[1][0])[::-1]
        self.asym_feature_list = feature_list

    """
    This method plot_pairs_feature export a pairs feature figure out to the default directory.
    The pairs feature is computed in the pairs_feature method and stored in the self.asym_feature_list.
    Argument:
    K:The top K pairs features to plot. When None, plot all the features.
    filter_biased_utterance: If True, the biased utterance, which means between two users only one of them talked,
    will be deleted from the plot. The remain of the plot dot only include those pair features that both of the users
    talked.
    """
    def plot_pairs_feature(self,K = None,filter_biased_utterance = False):
        pairs = list(map(lambda x:x[1],self.asym_feature_list))
        figure_name = 'Full Figure.png'
        if filter_biased_utterance:
            pairs = list(filter(lambda x:x[0] is not x[1],pairs))
            figure_name = 'Bias Filtered Figure.png'
        pairs = np.array(pairs)
        if K is None:
            plt.scatter(pairs[:,0],pairs[:,1])
        else:
            plt.scatter(pairs[:K,0],pairs[:K,1])
            plt.xlabel('Total directed utterance pairs.')
            plt.ylabel('Asymmetric')
        plt.savefig(figure_name)

    """
    This method is used to print the directed pairs' user information (user name or user id) in the text corpus.
    Argument:
    number_to_print: the maximum number of pairs to print, less then 100 is recommended.
    biased: If True, only the biased features will be printed. If False, only the unbiased features will be printed.
    """
    def show_filtered_utterance(self,number_to_print = 100,biased = True):
        for i in self.asym_feature_list:
            if (i[1][0] == i[1][1]) == biased:
                print(i[0])
                number_to_print -= 1
            if number_to_print == 0:
                break

        
            
        
                          
        
