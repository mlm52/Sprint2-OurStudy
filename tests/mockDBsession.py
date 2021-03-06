class MockSession:
    '''
    class to be used in tests to mock models.DB.session and its subsequent calls
    '''
    def __init__(self):
        return

    class query:
        def __init__(self, mocked_database_class):
            self.db = mocked_database_class._db_dict.copy()

        def filter_by(self, **kwargs):
            for attribute_name, attribute_value in kwargs.items():
                rows_to_remove = []
                for row in self.db:
                    try:
                        row_attribute = getattr(self.db[row], attribute_name)
                        if row_attribute != attribute_value:
                            rows_to_remove.append(row)
                    except AttributeError:
                        rows_to_remove.append(row)
                for row in rows_to_remove:
                    removed_value = self.db.pop(row, 'key not in dict')
                        
            return self

        def all(self):
            rows = []
            for key in self.db:
                rows.append(self.db[key])
            return rows

        def first(self):
            rows = []
            for key in self.db:
                rows.append(self.db[key])
                break
            if rows == []:
                return None
            else:
                return rows[0]

        def delete(self):
            rows_to_remove_locally = []
            for row in self.db:
                rows_to_remove_locally.append(row)
                self.db[row].remove()
            for row in rows_to_remove_locally:
                removed_value = self.db.pop(row, 'key not in dict')
        
        def count(self):
            return len(self.db)

    def add(self, mocked_database_row):
        mocked_database_row.add()

    def commit(self):
        pass

    def delete(self, mocked_database_row):
        mocked_database_row.remove()

    def refresh(self, mocked_database_row):
        pass
