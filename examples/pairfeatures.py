from convokit import Utterance, Corpus, Coordination, download, CountUtterance

corpus = Corpus(filename=download("supreme-corpus"),subdivide_users_by=["case","justice-is-favorable"])

cu = CountUtterance(corpus)

cu.print_report(10)

print('='*50)

U = list(corpus.all_users)
cu.directed_pairs(U[0],U[1],False,True)

print('='*50)

cu.pairs_feature()
cu.plot_pairs_feature()
cu.plot_pairs_feature(None,True)
cu.plot_pairs_feature(20)

cu.show_filtered_utterance(10)
cu.show_filtered_utterance(10,biased = False)



