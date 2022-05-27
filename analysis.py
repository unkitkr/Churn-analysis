from datetime import datetime
from itertools import count
import streamlit as st
import pandas as pd

st.title('Buffer churn analysis')
st.markdown("**Author: Ankit Kumar**")
st.markdown('''
    <style>
     .higlighted{
         color: #ff9966
     }
     a{
         color: #6e6e6e !important;
         text-transform: none !important;
     }
     a:hover{
         color: #8e8e8e !important;
         text-transform: underline
     }
    </style>




    #### __Table of contents__
    1. [Data Parameters](#1-data-parameters)
    2. [Framework for analysis](#2-framework-used-to-calculate-churn)
    3. [Data Cleaning](#3-data-cleaning)
    4. [Key Metrics]( #4-key-metrics)
    5. [Conclusion]( #5-conclusion)
    6. [Suggestions]( #6-suggestions)
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __1.__ __Data parameters__
    1. <span class = "higlighted">__Customer ID__</span> : The unique ID of the customer used across the internal buffer databases. This can help us understanding if the user was churned two or more times which indicates that those users gave Buffer two (or more) chances. This is critical since it means buffer has built trust among customers which gets them back to the platform but due to one (or more) reasons they churned.
    2. <span class = "higlighted">__Churn Date__</span> : The date when the customer churned. This parameter is very helpful to analyse several components of churn with respect to time. But since we are working with 6 month time frame, we won'use it much.
    3. <span class = "higlighted">__Plan Name__</span> : The name of the plan from which the customer churned out. This is particularly helpful to analyse which segment of users were churning and thereby helpful for speculating the root cause of the churn.
    4. <span class = "higlighted">__Amount__</span> : The amount of the plan which was churned by a customer. This metric can be used to calculate the net churn (financially) but deriving anything meaningful in terms of the reason of churn can be extremely difficult.
    5. <span class = "higlighted">__Churn Reason__</span> : User selected reason for churn. This is a key metric to understand user behaviour and particularly helpful to establish framework to analyse churn. However the granularity of the reason is low hence, there could be an explicit need to take some assumptions.
''', unsafe_allow_html = True)

st.markdown('''
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __2.__ __Framework used to calculate churn__
    \
                            
     1. Which customers are churning?
     2. Why are they churning?
     3. Customer behavior analysis
     4. Ways to reduce churn.

    
''', unsafe_allow_html = True)

st.markdown('''
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __3.__ __Data Cleaning (Long, may skip to [key metrics](#4-key-metrics))__
    \


    
''', unsafe_allow_html = True)

df = pd.read_csv('analyse.csv')
def date_convert(date):
    date_split = date.split(" ")
    month = int(datetime.strptime(date_split[0], "%b").strftime("%m"))
    date_ = int(date_split[1])
    year = int(datetime.strptime(date_split[2][1:], "%y").strftime("%Y"))
    new_date = datetime(year, month, date_).strftime('%d-%m-%Y')
    return new_date
df["Churn Date"] = df["Churn Date"].apply(date_convert)


st.markdown('''
    ###### __3.1.__ __Percentage of churns per plan__:
    \

    ''', unsafe_allow_html = True)

st.bar_chart(df["Plan Name"].value_counts(normalize=True).mul(100), use_container_width = True, height= 500)
st.markdown('''
    ###### __3.2.__ __Number of churns per plan__:
    \

    ''', unsafe_allow_html = True)
st.dataframe(df["Plan Name"].value_counts())
st.markdown('''
    \
    &nbsp;

    ###### __3.3.__ __Percentage of churn per reason__:
    
''', unsafe_allow_html = True)
st.bar_chart(df["Churn Reason"].value_counts(normalize=True).mul(100), use_container_width = True, height= 500)
st.markdown('''
    ###### __3.4.__ __Number of churns per Reason__:
    \

    ''', unsafe_allow_html = True)
st.dataframe(df["Churn Reason"].value_counts())
st.markdown('''
    \
    &nbsp;

    ###### __3.5.__ __Repeat customers__:
    
''', unsafe_allow_html = True)
last_dropped = df[df.duplicated(subset=['Customer ID'],keep= False)].drop_duplicates(subset=['Customer ID'], keep="last")
st.dataframe(last_dropped)
st.markdown('''
    \
    &nbsp;

    ###### __3.6.__ __Repeat customers last leaving reason__:
    
''', unsafe_allow_html = True)
st.bar_chart(last_dropped["Churn Reason"].value_counts())

st.markdown('''
    \
    &nbsp;

    ###### __3.7__ __Number of churns per plan per reason__:
    
''', unsafe_allow_html = True)

st.dataframe(df.groupby(["Plan Name", "Churn Reason"], as_index=False).size())

st.markdown('''
    \
    &nbsp;

    ###### __3.8.__ __Number of churns per plan per reason (multiple renewals)__:
    
''', unsafe_allow_html = True)

st.dataframe(last_dropped.groupby(["Plan Name", "Churn Reason"], as_index=False).size())

st.markdown('''
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __4.__ __Key metrics__
    \

''', unsafe_allow_html = True)

col1, col2 = st.columns(2)
col1.metric("Highest Churn (Plan)", "Pro8 v1 - Monthly", "-52.79%")
col2.metric("Highest Churn (Reason)", "Not using anymore", "-45.77%")
st.metric("Repeat Customers", "Customers who closed atleast two times", "-745")
col3, col4 = st.columns(2)
col3.metric("Highest churned reason(Second/third) time customers", "Not using anymore", "-745")
col4.metric("Highest churned plan(Second/third) time customers", "Pro8 v1 - Monthly", "-535")

st.markdown('''
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __5.__ __Conclusion__
    \

''', unsafe_allow_html = True)

st.markdown('''
    \
   
   To conclude we must draw a top level (an estimate) defination for each of the cancellation reason:
   1. <span class="higlighted">Not using anymore</span> : This is a generic case where in the action (opting out) can be cause by any factor except the reasons on other points. Example of cases where <span class="higlighted">Not using anymore</span> can be triggered by:
       * <u>The product introduced the feature which the customer was using on buffer</u>. Example: Twitter launced advanced analytics tools which made Buffers analytics tool an unused tool to them.
       * <u>The tools that they were already using offered them the tools which are present in buffer</u>. Example someone was using notion to plan thier content however notion released their public api hence they were able to use it to schedule those contents.
   2. <span class="higlighted">Extenuating circumstances</span>: This cannot be clearly defined however, depending on the circumstances there is a chance of retaining them because this necessarily doesn't mean they were unhappy with the product. It might come from the support they got or setting up a wrong expectation/success metric with the product.
   3. <span class="higlighted">Others</span>: This is the most generic response. however since there were other options present, we can clearly rule out the fact that the churn came from product related issues (missing features/bugs), to a large extent support related issues, price points, usage/usability issues. A few factors that can be considered here can be:
       * Customer ran out of business.
       * The product was not used much. Example they were in a business where social media presence didn't matter much.
       * Buffer was useful and priced properly, however the customer realized that ROI wasn't that great.
       * They moved to a competitor which provided them a generous trial period hence they churned and thought of giving them a shot.
      This list cann go long but we would focus on the event which likely caused churn because some issue on our side.
   4. <span class="higlighted">Too expensive</span>: Something which is a need can feel expensive only when cheaper options are available. Need to do a competitor analysis to establish a correalation, but surely this comes from companies which want to compete on price points.
   5. <span class="higlighted">Missing features</span>: This is coming from the fact that some features were so critical to some (a small subset) customers that they churned out. However this can also because of average price per feature. Not all features can be used by different subsets of customers with same degree of importance.
   6. <span class="higlighted">Missing features</span>: Not all customers can have tolerence to small glitches in software operations or the time taken to fix them. However doing a critical analysis of bugs can surely help.

   Analytically,
   1. The highest churn with respect to plan offering was: <span class="higlighted">Pro8 V1 -  monthly</span> (more than 50%), followed by same plan billed yearly.
   2. The highest churn with respect to customer reasoning was: <span class="higlighted">Not using anynmore</span> (close to 46%) followed by extenuating circumstances (~ 16%).
   3. A total of 745 customers had two (or more) churn entries. This was indicating they purchased the plan again. For a few customers there were three entries this indicated that customers came back thrice. This can indicate a few things:
       * There is a very strong product market fit and the product is bringing value.
       * The brand helps to sell the product because of marketing or word of mouth however it's not able to keep up with the expectations.
       * Customers are rationing their purchase. They get the product only and only when they need and opt out when the expectation is meet.
       * There can be an involuntary churn triggered by a credit card decline or accidentally user declined the payment.
   4. Out of those customers who churned out second/third time <span class="higlighted">Not using anymore</span> remains at the top.
   5. The correlation between the "churn reason" and "plan churned" is largely linear (Pro8 v1 - Monthly vs. not-using-anymore is at the top with 535 entries similarly for Pro8 v1 - yearly vs Not using anymore is at second with 212 entries)
   6. The trend went a bit off to the second time customers as we saw the plan offering majorly impacted was <span class="higlighted">Buffer Analyze - Full Price 10 Social Channels</span> because of the reason <span class="higlighted">not-using-anymore</span>, <span class="higlighted">where as Pro8 v1 - Monthly</span> was majorly churned because of being 'too expensive'.
''', unsafe_allow_html = True)

st.markdown('''
    &nbsp;
    \
    &nbsp;
    \
    &nbsp;

    ##### __6.__ __Suggestions__
    \

''', unsafe_allow_html = True)

st.markdown('''
    It is difficult to reach to a solid conclusion without having the life time value of customer of the days to churn number.
    However by analysing the current data that we have right now is:
    1. Need to focus on user retention by analysing the needs of the large amounts of customers signing up again. (aprox 745). These customer majorly left because of not using and price points. 
    2. Introducing more pricing tiers and pricing based on features. Especially for small businesses since they constitute a very large chunk, granularity in price can be boon for them and can give competitive advantage.
    3. Product on higher level looks good since the percentage of people churning because of bugs and missing features are relatively less (5% and 7%). Focusing on the current roadmap and especially on high ROI features can be more rewarding campared to focusing on a features demanded by a few customers.
    4. Need to do a close feature by price competitor analysis to make sure if we are up to datte and addressing the current demands of the customers.
    5. Studying churn behaviour more closely, may be by conducting interviews post churn or adding more options to the opt out form, add an option for customer to write their greviances if they choose to select <span class="higlighted">other</span> as option in the optout form to have a better cancellation insights.

''', unsafe_allow_html = True)