import convokit

#set up corpus
corpus = convokit.Corpus(filename=convokit.download("supreme-corpus") \
                         ,subdivide_users_by=["roots"])


#create count object
count = convokit.CountUtterance(corpus)

#report the result
count.print_report()
