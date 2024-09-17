import type { ComposerTranslation } from "vue-i18n";
import type { ShopWithOpenRange, OpenRange, Shop } from "./api/types";

function timeToMinutes(time: string): number {

    if (time.length === 16 || time.length === 19) { // Extract time from datetime string
        time = time.slice(11, 16);
    }
    else if (time.length === 8) { // HH:MM:SS
        time = time.slice(0, 5);
    }
    else if (time.length !== 5) {
        throw new Error('Invalid time format: ' + time);
    }
    const [hour, minute] = time.split(':').map(Number);
    return hour * 60 + minute;
}
function minutesToTime(minutes: number): string {
    const hour = Math.floor(minutes / 60)
        .toString()
        .padStart(2, '0');
    const minute = (minutes % 60).toString().padStart(2, '0');
    return `${hour}:${minute}`;
}

function reformatTime(time: string): string {
    if (time.length === 16 || time.length === 19) { // Extract time from datetime string
        time = time.slice(11, 16);
    }
    else if (time.length === 8) { // HH:MM:SS
        time = time.slice(0, 5);
    }
    else if (time.length !== 5) {
        throw new Error('Invalid time format: ' + time);
    }
    return time;
}

function DateToMinutes(date: Date): number {
    return date.getHours() * 60 + date.getMinutes();
}

function getDateOfWeek(y: number, w: number) {
    const date = new Date(y, 0, (1 + (w - 1) * 7)); // Elle's method
    date.setDate(date.getDate() + (1 - date.getDay())); // 0 - Sunday, 1 - Monday etc
    return date
}


function getDateOfWeekDay(y: number, w: number, d: number) {
    const date = new Date(y, 0, (1 + (w - 1) * 7)); // Elle's method
    date.setDate(date.getDate() + ((d + 1) - date.getDay()));
    return date
}

function getWeekDay(date: Date): number {
    return date.getDay() === 0 ? 6 : date.getDay() - 1;
}


function networkDateTime(date: Date) {
    if (!date) {
        date = new Date(0);
    }
    // get local timezone offset
    const offset = date.getTimezoneOffset();
    date.setMinutes(date.getMinutes() - offset);

    return date.toISOString().slice(0, 19);
}

function networkDate(date: Date) {
    if (!date) {
        date = new Date(0);
    }
    // get local timezone offset
    const offset = date.getTimezoneOffset();
    date.setMinutes(date.getMinutes() - offset);

    return date.toISOString().slice(0, 10);
}

function date_start_end(start: string, duration_minutes: number, locale: string): { date: string, start: string, end: string } {
    const d = new Date(start);
    return {
        date: d.toLocaleDateString(locale),
        start: start.slice(11, 16),
        end: minutesToTime(timeToMinutes(start.slice(11, 16)) + duration_minutes)
    }
}

function validateDates(shopData: ShopWithOpenRange | Shop | null | undefined, startTime: Date, endTime: Date, setError: (a: string | null) => void, day: number, week: number, year: number, $t: ComposerTranslation): boolean {
    if (!shopData) {
        setError($t('error.shop.not_loaded'));
        return false;
    }


    // Do not check the day if it is set to -1 or if the shop's data does not contain open_ranges
    if (day !== -1 && ("open_ranges" in shopData)) {
        const shopStart = (new Date(shopData.available_from)).getTime();
        const shopEnd = (new Date(shopData.available_until)).getTime();

        // Check that the start date is inside an open range
        const open_ranges = shopData?.open_ranges.filter(
            (range: OpenRange) => {
                const rangeDay = getDateOfWeekDay(year, week, range.day).getTime();
                return range.day === day && rangeDay >= shopStart && rangeDay <= shopEnd;
            }
        );

        if (!open_ranges.length) {
            setError($t('error.reservation.not_open_day'));
            return false;
        }

        if (!open_ranges.find(
            (range: OpenRange) => {
                const start_time = timeToMinutes(range.start_time);
                const end_time = timeToMinutes(range.end_time);
                const task_time = DateToMinutes(startTime);
                const task_time_end = DateToMinutes(endTime);

                return task_time >= start_time && task_time < end_time && task_time_end <= end_time;
            }
        )) {
            setError($t('error.reservation.not_open_time'));
            return false;
        }
    }

    const timeDiffMinutes = DateToMinutes(endTime) - DateToMinutes(startTime);

    if (timeDiffMinutes < 0) {
        setError($t('error.reservation.end_before_start'));
        return false;
    }


    if (timeDiffMinutes < shopData.min_time) {
        setError($t('error.reservation.too_short', { min_time: shopData.min_time }));
        return false;
    }

    if (timeDiffMinutes > shopData.max_time) {
        setError($t('error.reservation.too_long', { max_time: shopData.max_time }));
        return false;
    }

    setError(null);
    return true;
}

function formatDate(date: string): string {

    return date.slice(0, 10);
}

function DateToWeekNumber(date: Date): number {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
}

function maxDate(date1: Date, date2: Date): Date {
    return date1 > date2 ? date1 : date2;
}

function minDate(date1: Date, date2: Date): Date {
    return date1 < date2 ? date1 : date2;
}

export {
    timeToMinutes,
    minutesToTime,
    reformatTime,
    getDateOfWeek,
    getDateOfWeekDay,
    DateToMinutes,
    networkDateTime,
    networkDate,
    date_start_end,
    validateDates,
    getWeekDay,
    formatDate,
    DateToWeekNumber,
    maxDate,
    minDate
};