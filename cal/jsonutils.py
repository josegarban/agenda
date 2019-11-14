import json

def map_events(input_objectlist):
    """
    Input: events from query
    """
    dictlist = [e.to_dict() for e in input_objectlist]

    output = {}

    # Get all years in events only once
    years = list(output.keys())
    for e in dictlist:
        y_str = str(e['start_time'].year)
        if y_str not in years:
            output[y_str] = {}

    # Get all months with events in their respective years
    years = list(output.keys())
    for y in years:
        months = list(output[y].keys())
        for e in dictlist:
            m_str = str(e['start_time'].month - 1) #JS months start at 0
            if y == str(e['start_time'].year):
                if m_str not in months:
                    output[y][m_str] = {}

    # Get all days with events in their respective months and years
    for y in years:
        months = list(output[y].keys())
        for m in months:
            days = list(output[y][m].keys())
            for e in dictlist:
                d_str = str(e['start_time'].day)
                if y == str(e['start_time'].year) and m == str(e['start_time'].month - 1):
                    if d_str not in days:
                        output[y][m][d_str] = []

    # Append all events within a day
    for e in dictlist:
        y = str(e['start_time'].year)
        m = str(e['start_time'].month - 1) #JS months start at 0
        d = str(e['start_time'].day)

        e_dict = {}
        e_dict['displayname'] = e['title']
        e_dict['duration'] = int((e['end_time'] - e['start_time']).total_seconds() * 1000)
        e_dict['at'] = e['start_time'].strftime("%a %b %d %Y %H:%M:%S GMT%z")
        e_dict['id'] = e['id']

        output[y][m][d].append(e_dict)

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
