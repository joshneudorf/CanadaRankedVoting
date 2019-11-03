import pandas as pd
import numpy as np

results = pd.read_csv("2006.csv",sep=",")
print(results)
districts = results.district.unique()
print(len(districts))
results["winner"] = 0

left = ["Liberal","Green Party","N.D.P."]
right = ["People's Party","Conservative","Christian Heritage Party","Bloc Québécois","Parti Rhinocéros Party"]
results['party'] = ""
for p in left + right:
    results.loc[results['name'].str.contains(p),'party'] = p
results["vote_rank"] = 0
for d in districts:
    print(results.loc[(results['district'] == d)])
    votes_array = results.votes[results.district == d]
    temp = votes_array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(votes_array))
    ranks = len(ranks) - ranks
    results.loc[results.district == d, "vote_rank"] = ranks
    print(results.loc[(results['district'] == d)])
    left_highest = 100
    left_votes_p = 0
    left_votes = 0
    for l in left:
        if results.loc[(results['district'] == d) , "party"].str.contains(l).any():
            if results.loc[(results['district'] == d) & (results['party'] == l), "vote_rank"].iloc[0] < left_highest:
                left_highest = results.loc[(results['district'] == d) & (results['party'] == l), "vote_rank"].iloc[0]
                left_party = l
            left_votes_p += results.loc[(results['district'] == d) & (results['party'] == l), "percent_votes"].iloc[0]
            left_votes += results.loc[(results['district'] == d) & (results['party'] == l), "votes"].iloc[0]
            results.loc[(results['district'] == d) & (results['party'] == l), "percent_votes"] = 0
            results.loc[(results['district'] == d) & (results['party'] == l), "votes"] = 0
    results.loc[(results['district'] == d) & (results['party'] == left_party), "percent_votes"] = left_votes_p
    results.loc[(results['district'] == d) & (results['party'] == left_party), "votes"] = left_votes


    right_highest = 100
    right_votes = 0
    print("right")
    print(results.loc[(results['district'] == d) , "party"])
    for r in right:
        if results.loc[(results['district'] == d) , "party"].str.contains(r).any():
            if results.loc[(results['district'] == d) & (results['party'] == r), "vote_rank"].iloc[0] < right_highest:
                right_highest = results.loc[(results['district'] == d) & (results['party'] == r), "vote_rank"].iloc[0]
                right_party = r
            right_votes += results.loc[(results['district'] == d) & (results['party'] == r), "percent_votes"].iloc[0]
            results.loc[(results['district'] == d) & (results['party'] == r), "percent_votes"] = 0
    results.loc[(results['district'] == d) & (results['party'] == right_party), "percent_votes"] = right_votes

    votes_array = results.votes[results.district == d]
    temp = votes_array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(votes_array))
    ranks = len(ranks) - ranks
    results.loc[results.district == d, "vote_rank"] = ranks
    print(results.loc[(results['district'] == d)])
print(results)
results.loc[results.vote_rank == 1,"winner"] = 1
liberal_count = results.loc[results.party == "Liberal","winner"].sum()
ndp_count = results.loc[results.party == "N.D.P.","winner"].sum()
green_count = results.loc[results.party == "Green Party","winner"].sum()
conservative_count = results.loc[results.party == "Conservative","winner"].sum()
bloc_count = results.loc[results.party == "Bloc Québécois","winner"].sum()

print("Liberal: ",liberal_count,"NDP: ",ndp_count,"Green: ",green_count,"Conservative: ",conservative_count,"Bloc: ",bloc_count)
