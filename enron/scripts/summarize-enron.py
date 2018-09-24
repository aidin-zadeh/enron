import os, inspect
import argparse
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio


CURR_DIR = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
ROOT_DIR = os.path.dirname(CURR_DIR)

argparser = argparse.ArgumentParser(
    description="Create summary of Enron email correspondences",
    epilog="Example of use: `python -m enron.scripts.summarize --topn 5 --start 1998-05 --end 2002-12`"
)

argparser.add_argument(
    "-t",
    "--topn",
    type=int,
    default=5,
    help="Top-N sender. Default=`5`"
)

argparser.add_argument(
    "-s",
    "--start",
    type=str,
    default="1998-05",
    help="Start date in Year-Month. Default=1998-05"
)

argparser.add_argument(
    "-d",
    "--end",
    type=str,
    default="2002-12",
    help="End date in Year-Month. Default=2002-12"
)


def main(topn, start_ym, end_ym):
    # the most prolific senders, top-N senders

    # get data path
    path = os.path.join(ROOT_DIR, "data", "ext")

    # load recipients data
    ffname = os.path.join(path, "enron-recipients.csv")
    df_recipients = pd.read_csv(ffname, parse_dates=["datetime"])
    df_recipients.rename(columns={"recipient": "person"}, inplace=True)
    ffname = os.path.join(path, "enron-senders.csv")

    # load senders data
    df_senders = pd.read_csv(ffname, parse_dates=["datetime"])
    df_senders.rename(columns={"sender": "person"}, inplace=True)
    # get yearMonth attribute as "date"
    df_senders["date"] = df_senders.datetime.dt.to_period("M")
    df_recipients["date"] = df_recipients.datetime.dt.to_period("M")

    # group by person and  year-month dates
    gpby = [df_senders.person, df_senders.date]
    df_sender_counts = df_senders.groupby(gpby)["person"].count()
    df_sender_counts = df_sender_counts.to_frame(name="sent")

    # group by person and  year-month dates
    gpby = [df_recipients.person, df_recipients.date]
    df_recipient_counts = df_recipients.groupby(gpby)["person"].count()
    df_recipient_counts = df_recipient_counts.to_frame(name="received")

    # compute relative contact
    df_counts = df_sender_counts.join(df_recipient_counts, how="outer") \
        .fillna(0) \
        .applymap(lambda x: int(x)) \
        .sort_values(by="sent", ascending=False)

    df_counts["relcontact"] = (df_counts.received - df_counts.sent).abs() / \
        df_counts[["received", "sent"]].max(axis=1)

    # create/save person-sent summary data frame
    df_person_suammary = df_counts.reset_index()
    df_person_suammary = df_person_suammary.groupby(df_person_suammary.person)[["sent", "received"]] \
        .sum() \
        .reset_index() \
        .sort_values(by="sent", ascending=False) \
        .reset_index()
    # print(df_person_suammary.head())
    # save person-count summary
    ffname = os.path.join(ROOT_DIR, "data", "ext",
                          "enron-person-summary.csv")
    df_person_suammary[["person", "sent", "received"]].to_csv(ffname, index=False)

    # get the most prolific senders, top-N senders
    topn_senders = df_person_suammary.person[0:topn].tolist()

    # get top-N sender data
    df_topn = df_counts.loc[topn_senders, :].reset_index()
    df_topn.head(10)

    # Compute relative contact
    df_counts["relcontact"] = (df_counts.received - df_counts.sent).abs() / \
        df_counts[["received", "sent"]].max(axis=1)

    # plot sent trends
    colors = list(range(40))
    title = "Number of emails sent by top-" + \
            str(topn) + " senders between '" + start_ym + "' and '" + end_ym
    colors = [" #ff0000", "#b2004c", "#8c0073", "#5900a6", "#0000ff"]
    idx = pd.date_range(start=start_ym, end=end_ym, freq='MS').to_period("M")

    data = []

    for i in range(0, topn):
        df_i = df_counts.loc[topn_senders[i], :]
        df_i = df_i.reindex(idx, fill_value=0)

        trace = go.Scatter(
            x=list(df_i.index.astype(str).values),
            y=df_i.sent,
            name=topn_senders[i].title(),
            line=dict(color=colors[i]),
            opacity=0.9,
            mode="lines"
        )

        data.append(trace)

    layout = dict(
        title=title,
        yaxis=dict(title='# Emails Sent'),
        xaxis=dict(
            title="Time",
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    annotations = []
    layout['annotations'] = annotations

    fig = dict(data=data, layout=layout)
    ffname = os.path.join("images", "sent-emails-plot")
    pio.write_image(fig, ffname + ".png")
    py.plot(fig, filename="Sent Email Count")

    # plot relative-ratio trends
    title = "Relative Contact Ratio by top-" + \
            str(topn) + " senders between '" + start_ym + "' and '" + end_ym
    colors = [" #ff0000", "#b2004c", "#8c0073", "#5900a6", "#0000ff"]
    idx = pd.date_range(start='1998-05', end="2002-12", freq='MS').to_period("M")

    data = []

    for i in range(0, topn):
        df_i = df_counts.loc[topn_senders[i], :]
        df_i = df_i.reindex(idx, fill_value=0)

        trace = go.Scatter(
            x=list(df_i.index.astype(str).values),
            y=df_i.relcontact,
            name=topn_senders[i].title(),
            line=dict(color=colors[i]),
            #         colorscale='Viridis',
            opacity=0.9,
            mode="lines"
        )

        data.append(trace)

    layout = dict(
        title=title,
        yaxis=dict(title='Contact Relative Ratio'),
        xaxis=dict(
            title="Time",
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    annotations = []

    layout['annotations'] = annotations

    fig = dict(data=data, layout=layout)
    ffname = os.path.join("images", "relative-contact-plot")
    pio.write_image(fig, ffname + ".png")
    py.plot(fig, filename="Relative Contact Ratio")


if __name__ == "__main__":
    global args
    args = argparser.parse_args()
    topn = args.topn
    start_ym = args.start
    end_ym = args.end
    main(topn, start_ym, end_ym)

