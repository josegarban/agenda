import json

def events_to_dict(input_objectlist):
    """
    Input: events from query
    """
    dictlist = [e.to_dict() for e in input_objectlist]

    output = {}

    days = []
    for e in dictlist:
        day_str = str(e['start_time'].day)
        days.append(day_str)
        output[day_str] = []

    for e in dictlist:
        e_dict = {}
        e_dict['displayname'] = e['title']
        e_dict['duration'] = int((e['end_time'] - e['start_time']).total_seconds() * 1000)
        e_dict['at'] = e['start_time'].strftime("%a %b %d %Y %H:%M:%S GMT%z")
        day_str = str(e['start_time'].day)

        for d in days:
            if d == day_str:
                output[day_str].append(e_dict)

    # return output
    return json.dumps(output)


"""
output example

matrix[today.getFullYear()] = {};

matrix[today.getFullYear()][today.getMonth()] = {
    "5"  : [{displayname : "You can't miss this event", color : "#792aca"}],
    "12" : [
    {
        displayname : "A very important meeting",
        at : new Date(today.getFullYear(), today.getMonth(), 12, 15, 30).getTime()
    },
    {
        displayname : "A somewhat important 2 hours meeting",
        color : "rgb(113, 180, 193)",
        at : new Date(today.getFullYear(), today.getMonth(), 12, 17, 30).getTime(),
        duration : 1000 * 60 * 60 * 2
    },
    {
        displayname : "This meeting is so important it's red",
        color : "#9c3d27",
        at : new Date(today.getFullYear(), today.getMonth(), 12, 21, 55).toString()
    }
    ],
    "15" : [
    {
        displayname : "Something else to do here",
        at : new Date(0, 0, 0, 9, 30).toString()
    },
    {
        displayname : "Similar event",
        at : new Date(0, 0, 0, 9, 50).toString(),
        duration : 1000 * 60 * 10,
        color : "#5198da"
    }
    ],
    "16" : [{displayname : "Something to do here"}],
    "17" : [{at : new Date(0, 0, 0, 10, 25).getTime()}],
    "26" : [
    {
        displayname : "An event by the end of the month",
        at : new Date(0,0,0, 9)
    }
    ],
    "27" : [
    {
        displayname : "Short monthly recap meeting",
        at : new Date(0,0,0, 15, 30),
        color : "rgb(113, 180, 193)",
        duration : 1000 * 60 * 30
    }
    ]
};
"""
