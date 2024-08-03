function timeToMinutes(time: string): number {
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

export { timeToMinutes, minutesToTime };