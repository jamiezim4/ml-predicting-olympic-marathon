import numpy

def mergeListsToMap(keyList, valuesList):
    if len(keyList) != len(valuesList):
        raise ValueError('lists are not same length')
    i = 0
    records = {}
    for i in range(len(keyList)):
        records[keyList[i]] = valuesList[i]
    return records

def transform_data_point_result_time(predicted_time):
    predicted_time_delta = numpy.timedelta64(int(predicted_time[0]), 'ns')
    whole_hours = predicted_time_delta.astype('timedelta64[h]')
    predicted_time_delta -= whole_hours
    whole_minutes = predicted_time_delta.astype('timedelta64[m]')
    predicted_time_delta -= whole_minutes
    whole_seconds = predicted_time_delta.astype('timedelta64[s]')
    return '%02d:%02d:%02d' % (whole_hours.astype(int), whole_minutes.astype(int), whole_seconds.astype(int))