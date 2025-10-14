/**
 * Утилиты для работы с датами
 */

/**
 * Форматирует дату периода в читаемый формат
 * @param periodMonth - строка с датой в различных форматах
 * @param options - опции форматирования
 * @returns отформатированная строка с датой
 */
export const formatPeriodDate = (
  periodMonth: string, 
  options: {
    includeTime?: boolean;
    monthFormat?: 'long' | 'short';
  } = {}
): string => {
  const { includeTime = true, monthFormat = 'long' } = options;
  
  try {
    let dateValue = periodMonth;
    
    // Нормализуем различные форматы дат
    if (dateValue.length === 7) {
      dateValue = `${dateValue}-01T00:00:00`;
    } else if (dateValue.length === 10) {
      dateValue = `${dateValue}T00:00:00`;
    } else if (dateValue.length === 16) {
      dateValue = `${dateValue}:00`;
    }
    
    const date = new Date(dateValue);
    
    const formatOptions: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: monthFormat,
      day: 'numeric',
    };
    
    if (includeTime) {
      formatOptions.hour = '2-digit';
      formatOptions.minute = '2-digit';
    }
    
    return date.toLocaleString('ru-RU', formatOptions);
  } catch {
    return periodMonth;
  }
};

/**
 * Получает предыдущий месяц для заданной даты периода
 * @param periodMonth - строка с датой периода
 * @param options - опции форматирования
 * @returns отформатированная строка с предыдущим месяцем
 */
export const formatPreviousPeriodDate = (
  periodMonth: string,
  options: {
    includeTime?: boolean;
    monthFormat?: 'long' | 'short';
  } = {}
): string => {
  const { includeTime = true, monthFormat = 'long' } = options;
  
  try {
    let dateValue = periodMonth;
    
    // Нормализуем различные форматы дат
    if (dateValue.length === 7) {
      dateValue = `${dateValue}-01T00:00:00`;
    } else if (dateValue.length === 10) {
      dateValue = `${dateValue}T00:00:00`;
    } else if (dateValue.length === 16) {
      dateValue = `${dateValue}:00`;
    }
    
    const date = new Date(dateValue);
    const prevMonth = new Date(date.setMonth(date.getMonth() - 1));
    
    const formatOptions: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: monthFormat,
      day: 'numeric',
    };
    
    if (includeTime) {
      formatOptions.hour = '2-digit';
      formatOptions.minute = '2-digit';
    }
    
    return prevMonth.toLocaleString('ru-RU', formatOptions);
  } catch {
    return periodMonth;
  }
};
