// 时间处理工具函数

import dayjs from 'dayjs';
import timezone from 'dayjs/plugin/timezone';
import utc from 'dayjs/plugin/utc';

// 配置dayjs
dayjs.extend(utc);
dayjs.extend(timezone);

// 设置默认时区为澳大利亚悉尼
const DEFAULT_TIMEZONE = 'Australia/Sydney';

/**
 * 格式化时间
 */
export function formatTime(date: string | Date, format = 'YYYY-MM-DD HH:mm:ss'): string {
  return dayjs(date).tz(DEFAULT_TIMEZONE).format(format);
}

/**
 * 获取当前时间
 */
export function getCurrentTime(): string {
  return dayjs().tz(DEFAULT_TIMEZONE).format('YYYY-MM-DD HH:mm:ss');
}

/**
 * 时间转像素位置
 */
export function timeToPx(time: string | Date, timelineStart: string | Date, pixelsPerHour: number): number {
  const minutesPerPixel = 60 / pixelsPerHour;
  const diffMinutes = dayjs(time).diff(dayjs(timelineStart), 'minute');
  return diffMinutes / minutesPerPixel;
}

/**
 * 像素位置转时间
 */
export function pxToTime(pixels: number, timelineStart: string | Date, pixelsPerHour: number): string {
  const minutesPerPixel = 60 / pixelsPerHour;
  const diffMinutes = pixels * minutesPerPixel;
  return dayjs(timelineStart).add(diffMinutes, 'minute').format('YYYY-MM-DD HH:mm:ss');
}

/**
 * 获取时间范围
 */
export function getDefaultTimeRange(): { start: string; end: string } {
  const now = dayjs();
  const yesterday = now.subtract(1, 'day').hour(21).minute(0).second(0);
  const threeDaysLater = now.add(3, 'day').hour(3).minute(0).second(0);
  
  return {
    start: yesterday.format('YYYY-MM-DD HH:mm:ss'),
    end: threeDaysLater.format('YYYY-MM-DD HH:mm:ss')
  };
}

/**
 * 计算时间差（分钟）
 */
export function diffMinutes(start: string | Date, end: string | Date): number {
  return dayjs(end).diff(dayjs(start), 'minute');
}

/**
 * 判断是否为今天
 */
export function isToday(date: string | Date): boolean {
  return dayjs(date).isSame(dayjs(), 'day');
}

/**
 * 判断是否为今天或之前
 */
export function isTodayOrBefore(date: string | Date): boolean {
  return dayjs(date).isSameOrBefore(dayjs(), 'day');
}
