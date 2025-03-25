# crud.py
from backend.database import supabase

class DatabaseService:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def create(self, data: dict):
        """Thêm một bản ghi vào bảng"""
        response = supabase.table(self.table_name).insert(data).execute()
        return response

    def get_all(self):
        """Lấy tất cả bản ghi"""
        response = supabase.table(self.table_name).select("*").execute()
        return response

    def get_by_field(self, field: str, value):
        """Tìm bản ghi theo một field cụ thể"""
        response = supabase.table(self.table_name).select("*").eq(field, value).execute()
        return response

    def update(self, filters: dict, data: dict):
        """Cập nhật bản ghi dựa trên filters (VD: {"id": "123"})"""
        query = supabase.table(self.table_name).update(data)
        for field, value in filters.items():
            query = query.eq(field, value)
        response = query.execute()
        return response

    def delete(self, filters: dict):
        """Xóa bản ghi dựa trên filters"""
        query = supabase.table(self.table_name).delete()
        for field, value in filters.items():
            query = query.eq(field, value)
        response = query.execute()
        return response
