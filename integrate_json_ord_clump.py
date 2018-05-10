import math

def integrate_single_channel(vals,t):
    # vals is a list of floats
    # t is a float
    # this integrates vals over t
    # the value of the first 1/5 of vals is averaged to find a background level
    # the result of the integration is returned
    stop = int(math.ceil(len(vals)/5))
    # stop is the index of the end of the first 5th of vals
    ave = 0.0
    for i in range(stop):
        ave += vals[i]
    ave /= float(stop)
    # ave is now the average value of the first 5th of the data
    # now we integrate, by left side Riemann
    total = 0.0
    for i in range(stop,len(vals)):
        total += (vals[i]-ave)*t
        # by subtracting ave we remove any static vertical offset
        # leaving only the signal plus noise
    return total

def integrate_json_ord_clump(ev,t):
    # ev is a list of events as they are save in json ord clump format
    # t is the time between measurements, saved encoded as a float
    # this function returns a list of dicts
    # each of those dicts correstponts to an event
    # the keys to the dicts are integers representing channels
    # the values are the value of that channel integrated over time
    ou = []
    for event in ev:
        da = event["DATA"]
        # da is now a dict mapping string channels to lists of floats
        q = dict()
        for ch in da:
            q[int(ch)] = integrate_single_channel(da[ch],t)
            # this adds an integer->float entry to q with the integration result for a channel
        ou.append(q)
    return ou
