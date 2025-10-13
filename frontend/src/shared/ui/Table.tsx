import type { TableColumn } from './types';

interface TableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  emptyMessage?: string;
  onRowClick?: (item: T) => void;
  className?: string;
}

function Table<T extends Record<string, any>>({
  data,
  columns,
  loading = false,
  emptyMessage = 'Нет данных',
  onRowClick,
  className = ''
}: TableProps<T>) {
  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border border-secondary-200 ${className}`}>
        <div className="p-8 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-2 text-sm text-secondary-500">Загрузка...</p>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border border-secondary-200 ${className}`}>
        <div className="p-8 text-center">
          <p className="text-secondary-500">{emptyMessage}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-secondary-200 overflow-hidden ${className}`}>
      <div className="overflow-x-auto">
        <table className="table">
          <thead>
            <tr>
              {columns.map((column, index) => (
                <th key={index} className="text-left">
                  {column.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item, rowIndex) => (
              <tr
                key={rowIndex}
                className={onRowClick ? 'cursor-pointer hover:bg-secondary-50' : ''}
                onClick={() => onRowClick?.(item)}
              >
                {columns.map((column, colIndex) => (
                  <td key={colIndex}>
                    {column.render
                      ? column.render(item[column.key], item)
                      : item[column.key]
                    }
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Table;
