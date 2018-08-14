# Author: Surayez Rahman
# Created on: 4th August, 2018
# Topic: MATLAB code written by Lachlan Andrew to detect edges, converted to Python

import math
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

def find_edges(userData=None, meta=None):
    #%%
    # TODO:
    # - discount "reliability" of runs near wake-up time, especially winter
    # - select which rectangles are "HWS" (or at least grouped, using AIC)
    # - if reliability high, coerce match_jump to select an existing run
    # - Align rectangles.  How?
    # - Confidence of rectangles.  How?
    # - day-of-week
    # - Adaptive: if "spike then flat" found in some runs, look for it elsewhere
    #             if day-of-week found in some runs, look for it elsewhere
    #             if overnight found in some runs, look for it elsewhere
    #             if morning/afternoon operation found, look for it elsewhere
    #             if miss one block, look for it in other blocks of the same day
    # - fill gaps

    # Terms:
    #   run -- consecutive days with a given jump
    #   reliability -- confidence that a run is from a timed device
    #   rectangle -- consecutive days with a given turn-on and matching turn-off
    #   quality/trust -- confidence that a rectangle is actually a timed device
    #   quality -- confidence that the end of a rectangle is the true end?

    # Columns in "runs"
    # 1. start day  (first day of run)
    # 2. stop day   (first day after run)
    # 3. half-hour slot
    # 4. half-hour slot, interpolated
    # 5. jump (increase in power)
    # 6. jump, as estimated from interpolated time
    # 7. reliability
    # 8. trend (average increase based on previous and subsequent slots)


    c = stripSpikes(squeeze(userData))

    valid_days = find(not isnan(c(1, [:])))
    cc = c(mslice[:], valid_days)

    if isempty(cc):
        return

    # Try to guess when the pump is on.
    # Some pumps have two (or more?) powers, so record time and value

    [runs, d, dd, band] = runs_from_cc(cc, meta)

    # Merge runs oscillating between neighbouring times
    runs = merge_oscillating_runs(runs, cc, dd, band)

    # Merge adjacent runs if that seems suitable
    runs = merge_adjacent_runs(runs, cc, dd, band)

    show_runs(runs, c, valid_days)


def runs_from_cc(cc=None, meta=None):
    # Extract time/start-day/end-day runs from 2-D array of jump sizes
    d1 = mcat([0, OMPCSEMI, diff(cc(mslice[:]))])
    d1(1).lvalue = d1(1 + meta.SamPerDay * (size(cc, 2) > 1))# guess first jump
    d = reshape(d1, size(cc))# half-hour differences
    # create a band around midnight for identifying steps
    band = 2
    dd = mcat([d, OMPCSEMI, d(mslice[1:2 * band], mslice[:])])
    variance_by_hour = var(diff(cc.cT))
    med_lengths = mcat([5, 7, 9, 11, 13, 15, 17, 19, 21])
    length_bins = min(1 + floor(variance_by_hour * 5), length(med_lengths))
    smoothed_c = zeros(size(cc))
    for i in mslice[1:length(med_lengths)]:
        idx = (length_bins == i)
        smoothed_c(idx, mslice[:]).lvalue = -rolling_min(-rolling_min(cc(idx, mslice[:]).cT, med_lengths(i)), med_lengths(i)).cT

    times    find_jumps(smoothed_c, 0.05, 1)

    sp = sparse(mod(round(times), size(cc, 1)) + 1, floor(round(times) / size(cc, 1)) + 1, jp, size(smoothed_c, 1), size(smoothed_c, 2))
    sp = sparse(medfilt1(full(sp), 9, mcat([]), 2))
    runs = runs_from_sparse(sp, dd, cc, band)


def show_runs(runs=None, c=None, valid_days=None):
    tmp = zeros(size(c))
    for j in mslice[1:size(runs, 1)]:
        if runs(j, 3) != -1:
            tmp(runs(j, 3), valid_days(mslice[runs(j, 1):runs(j, 2) - 1])).lvalue = runs(j, 7) * sign(runs(j, 5))

    plt.figure(2)
    plt.plot()
    plt.show()

    imagesc(tmp)

    plt.figure(3)
    plt.plot()
    plt.show()


def get_weighted_edge(time=None, data=None, power=None, g=None, offset=None, turn_on=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # A transition part way through an interval causes a mid-level power
    # Is floor(time) the mid point or end of the transition?
    if abs(time - round(time)) < 0.2:
        mid = round(time) + mcat([-1, 0])
    else:    # time middle of the interval: floor(time) is the mid-point
        mid = math.floor(time)

    if any(mid <= 0):
        mid = mid + size(data, 1) / 2


    # f
    wgts = zeros(length(mid), size(data, 2))
    for m in mslice[1:length(mid)]:
        #transition = data(mid(m));
        after = (mslice[mid(m) + 1:mid(m) + g])    # periods before and after.  Element 1
        before = (mslice[mid(m) - 1:-1:mid(m) - g])    # is closest to the transition in both
        if before(end) <= 0:
            before = before + size(data, 1) / 2

        if turn_on:
            is_off = data(before, mslice[:])
            is_on = data(after, mslice[:])
        else:
            is_off = data(after, mslice[:])
            is_on = data(before, mslice[:])


        wgts(m, mslice[:]).lvalue = 1 /eldiv/ (offset + (is_off(1, mslice[:])) / power) + 0.5 /eldiv/ (1 + (max(is_off, mcat([]), 1) - min(is_off, mcat([]), 1)) / power) + 0.5 /eldiv/ (1 + (max(is_on, mcat([]), 1) - min(is_on, mcat([]), 1)) / power)


    w = sum(wgts, 2)
    max(w)# pick time that looks most like a transition
    #w    = w   (mx);
    mid = mid(mx)
    wgts = wgts(mx, mslice[:])

# after
    data(mid - 1 + size(data, 1) / 2, mslice[:])# before
    # middle
    frac = (p3(3) - p3(1)) / (p3(2) - p3(1))
    t = mid + max(0, min(1, frac))
    if t < 0.5:
        t = t + size(data, 1) / 2
    elif t > size(data, 1) / 2 + 0.5:
        t = t - size(data, 1) / 2

    if mid > 1:
        jumps = data(mid + 1, mslice[:]) - data(mid - 1, mslice[:])
    else:
        jumps = data(mid + 1, mslice[:]) - data(mid - 1 + size(data, 1) / 2, mcat([mslice[2:end], end]))


def not_ramp(time=None, on_off=None, days=None, cv=None):
    # Score from 1 if cv(time, days) looks like a two-part step,
    # to 0 if it looks like a linear change.
    # time is the nominal time of the step
    # on_off is 1 for turning on, -1 for turning off
    # days is the range of days that the step/ramp occurs
    # cv is either cv or cvw.

    # Turn time into a string of four half-hours,
    # starting from the "off" state and ending one step after the end of the
    # transition.
    time = floor(time * on_off) - 1
    time = mod1((mslice[time:time + 3]) * on_off, size(cv, 1))
    low_to_high = cv(time, days)

    means = mean(low_to_high, 2)
    vars = var(low_to_high, 0, 2)

    mean_last_two = (vars(end - 1) * means(end - 1) + vars(end) * means(end)) / (vars(end - 1) + vars(end))
    badness1 = sum((means(mslice[end - 1:end]) - mean_last_two) **elpow** 2 /eldiv/ vars(mslice[end - 1:end])) / 2

    # Least square linear regression
    sum_a = sum(1 /eldiv/ vars)
    sum_ia = sum((mslice[1:length(vars)]) /eldiv/ vars.cT)
    sum_i2a = sum((mslice[1:length(vars)]) **elpow** 2 /eldiv/ vars.cT)
    sum_y = sum(means /eldiv/ vars)
    sum_iy = sum((mslice[1:length(vars)]).cT *elmul* means /eldiv/ vars)
    coeffs = mcat([sum_a, sum_ia, OMPCSEMI, sum_ia, sum_i2a]); print coeffs
    mcat([sum_y, OMPCSEMI, sum_iy])

    linear_fit = coeffs(1) + (mslice[1:length(vars)]).cT * coeffs(2)

    badness2 = sum((means - linear_fit) **elpow** 2 /eldiv/ vars) / 4

    score = badness2 / (badness1 + badness2)

    ds = mcat([1 / badness1, OMPCSEMI, 1, OMPCSEMI, 1 / badness2])
    ds = ds / sum(ds)


def stripSpikes(c=None, peakRatio=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if nargin < 2:
        peakRatio = 5

    idx = find(c(mslice[2: - 1]) - c(mslice[1: - 2]) > peakRatio * abs(c(mslice[3:]) - c(mslice[1: - 2])))
    base = c
    base(idx + 1).lvalue = (c(idx) + c(idx + 2)) / 2
    if nargout > 1:
        spikes = c - base



samPerDay
# (~ is 'c')
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tm = run(3)
st = run(1); print st
en = run(2) - 1

tt = mod1(tm - band, samPerDay)
slice = d(mslice[tt:tt + 2 * band], mslice[st:en])
slice = slice(mslice[:], not isnan(slice(1, mslice[:])))# Ignore entirely-NaN days

#jp = mean(slice(band+1,:));
#sd = sqrt(var(slice(band+1,:) ));

# Process a band around this run, to see if the jump is "significant"
jp_all = mean(slice, 2)
sd_all = sqrt(var(slice, mcat([]), 2))
sd = sd_all(band + 1)
jp = jp_all(band + 1)
trend = sum(jp_all - jp) / (2 * band)

# If jump is in the middle of the measurement slot, it affects two rows
jp_all(sd_all > abs(jp_all)).lvalue = 0# ignore this row if jump < noise
neighbours = jp_all(mcat([band, band + 2]))# one above / one below
min(abs(jp - neighbours))
jp_better = jp_all(better)
if sign(jp_better) == sign(jp) and (sign(jp_better) != sign(trend) or abs(jp_better) > 2 * abs(trend)) and (jp_better + jp) != 0:
    tm_real = tm + 2 * (better - 1.5) * (jp_better / (jp_better + jp))
    jp_real = jp + jp_better
else:
    tm_real = tm
    jp_real = jp

reliability = abs(jp - trend) * sqrt(en - st) / (sd + 1e-12)
if en - st < 5 and reliability > 14:# less than "significance" threshold,
    reliability = 14# but still may match a significant jump


def runs_from_sparse(sp=None, dd=None, c=None, band=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    runCount = 0
    runs = zeros(2 * size(c, 1), 3)
    # Find "runs": clusters of consecutive days with a jump at the same time
    for i in mslice[1:size(c, 1)]:
        d = diff(sp(i, mslice[:]) != 0)
        swap = (sign(sp(i, mslice[1:end - 1])) *elmul* sign(sp(i, mslice[2:end])) == -1)
        if not any(d):
            if (sp(i, 1) != 0 and not isnan(sp(i, 1))):
                starts = 1
                ends = size(c, 2) + 1
            else:
                continue
            end
        else:
            starts1 = find(logical_or(d > 0, swap)) + 1        # first day of run
            ends1 = find(logical_or(d < 0, swap)) + 1        # first day after run
            if isempty(starts1):
                starts1 = 1

                ends1 = size(c, 2) + 1
            end
            if ends1(1) <= starts1(1):
                starts = mcat([1, starts1])            # starts1 and ends1 to avoid Matlab warning
            else:
                starts = starts1
            end

            ends = mcat([end, s1, size(c, 2) + 1])
        else:
            ends = ends1
        end
        # Delete intervals that are all NaN
        if any(isnan(sp(i, mslice[:]))):
            allNaN = zeros(size(starts))
            for j in mslice[1:length(starts)]:

                allNaN(j).lvalue = 1
            end

        starts = starts(not allNaN)
        ends = ends(not allNaN)



L = length(starts)
if L > 0:
    runs(runCount + (mslice[1:L]), mslice[:]).lvalue = mcat([starts.cT, end, s.cT, repmat(i, mcat([L, 1]))])
    runCount = runCount + L


runs = runs(mslice[1:runCount], mslice[:])# truncate excess pre-allocated space

# If any run is long, calculate "reliability" of all runs
if max(runs(mslice[:], 2) - runs(mslice[:], 1)) > 14:
    for i in mslice[1:runCount]:
        [tm_real, jp, jp_real, reliability, trend] = find_reliability(runs(i, mslice[:]), dd, c, size(c, 1), band)
        runs(i, mslice[4:8]).lvalue = mcat([tm_real, jp, jp_real, reliability, trend])

else:
    runs(mslice[:], mslice[4:8]).lvalue = 0# if all short, skip that step


if runCount > 0:
    runs = runs(not isnan(runs(mslice[:], 7)), mslice[:])
    runCount = size(runs, 1)
else:
    runs = zeros(0, 8)# Octave complains if 0x8 is compared with say 0x4



def merge_oscillating_runs(runs=None, cc=None, dd=None, band=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Merge runs oscillating between neighbouring times
    runCount = size(runs, 1)
    toDelete = zeros(1, runCount)
    for i in mslice[1:runCount]:
        if runs(i, 3) < 0:        # if already flagged for deletion
            continue


        # Find runs that occur immediately after run i.
        if runs(i, 2) < size(cc, 2) + 1:
            after1 = runs(mslice[:], 1) == runs(i, 2)
            after2 = after1
            if runs(i, 3) > 2:
                after1 = logical_and(after1, (abs(runs(mslice[:], 3) - runs(i, 3)) == 1))

            if runs(i, 3) < size(cc, 1) + 1:
                after2 = logical_and(after2, (abs(runs(mslice[:], 3) - runs(i, 3)) == 1))

            after = find(logical_or(after1, after2))
        else:
            after = mcat([])


        rm = runs(i, 7)
        rt = 0
        rr = mcat([])
        for k in mslice[1:length(after)]:
            a = after(k)
            last = runs(a, 2)
            aa = find(runs(mslice[:], 3) == logical_and(runs(i, 3), runs(mslice[:], 1) == runs(a, 2)))
            if not isempty(aa):
                if length(aa) > 1:
                    # Multiple overlapping "runs"
                    # Merge with most reliable previous one
                    max(runs(aa, 7))
                    aa = aa(r)

                last = runs(aa, 2)


            run = mcat([runs(i, 1), last, runs(i, 3)])
            [x1, x2, x3, r, x4] = find_reliability(run, dd, cc, size(cc, 1), band)
            if r > rm and r > runs(a, 7) and (isempty(aa) or r > runs(aa, 7)):
                rr = mcat([a, aa])
                rt = runs(i, 3)
                rm = r
                x = mcat([x1, x2, x3, x4])

            run = mcat([runs(i, 1), runs(a, 2), runs(a, 3)])
            [x1, x2, x3, r, x4] = find_reliability(run, dd, cc, size(cc, 1), band)
            if r > rm and r > runs(a, 7):
                rr = a
                rt = runs(a, 3)
                rm = r
                x = mcat([x1, x2, x3, x4])


        if rm > runs(i, 7):
            if rr(1) < i:
                toDelete(i).lvalue = 1
                runs(i, 3).lvalue = -1
                toExtend = rr(1)
            else:
                toDelete(rr(1)).lvalue = 1
                runs(rr(1), 3).lvalue = -1
                toExtend = i
            end
            runs(toExtend, 1).lvalue = runs(i, 1)
            runs(toExtend, 2).lvalue = runs(rr(end), 2)
            runs(toExtend, 3).lvalue = rt
            runs(toExtend, mslice[4:8]).lvalue = mcat([x(1), x(2), x(3), rm, x(4)])
            if length(rr) > 1:
                toDelete(rr(2)).lvalue = 1
                runs(rr(2), 3).lvalue = -1

    runs = runs(not toDelete, mslice[:])



def merge_adjacent_runs(runs=None, cc=None, dd=None, band=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    sorted(runs(mslice[:], 3) + runs(mslice[:], 1) / size(cc, 2))
    runs = runs(idx, mslice[:])
    if (size(runs, 1) > 1):
        candidates = find(diff(runs(mslice[:], 3)) == logical_and(0, diff(sign(runs(mslice[:], 5))) == logical_and(0, (logical_or(runs(mslice[1:end - 1], 7) > 10, runs(mslice[2:end], 7) > 10)))))
        for i in candidates(mslice[:]).cT:
            st = runs(i, 2)
            en = runs(i + 1, 1)
            row = runs(i, 3)
            prev = mod1(row - 1, size(cc, 1))
            if runs(i, 5) < 0:
                top = prev
            else:
                top = row
            end
            if (all(cc(top, mslice[st:end]) > max(runs(mslice[i:i + 1], 5))) and en - st < 0.2 * mean(runs(mslice[i:i + 1], 2) - runs(mslice[i:i + 1], 1)) and sign(mean(cc(row, mslice[st:end]) - cc(prev, mslice[st:end]))) == sign(runs(i, 5))):
                run = mcat([runs(i, 1), runs(i + 1, 2), row])
                [x1, x2, x3, x4, x5] = find_reliability(run, dd, cc, size(cc, 1), band)
                if x4 > runs(i, 7):
                    # merge into i+1, which is further checked next iter'n
                    runs(i + 1, 1).lvalue = runs(i, 1)
                    runs(i + 1, mslice[4:8]).lvalue = mcat([x1, x2, x3, x4, x5])
                    runs(i, 3).lvalue = -1                # flag for deletion

    runs = runs(runs(mslice[:], 3) != -1, mslice[:])
    # delete runs flagged above for deletion


# Modulo, 1..modulus, not 0..modulus-1 (Matlab's arrays start from 1)
def mod1(value=None, modulus=None):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Modulo operator, returning values in [1, modulus], not [0, modulus-1].
    m = ((value - 1) % modulus) + 1
