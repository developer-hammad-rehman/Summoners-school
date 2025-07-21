import pytest
from httpx import AsyncClient

base_url = "http://localhost:8000/api"

# Helper to create a valid course
async def create_course_helper():
    data = {
        "name": "Demo",
        "rating": 4.067,
        "owner": {
            "id": 45500,
            "name": "Demo Owner"
        },
        "view": 800000,
        "price": 25.899,
        "type": "popular"
    }
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/course/create", json=data)
        assert response.status_code == 200
        return response.json()

# ✅ Test course creation
@pytest.mark.asyncio
async def test_create_course():
    course = await create_course_helper()
    assert "_id" in course
    assert isinstance(course["_id"], str)
    assert len(course["_id"]) == 24
    assert course["name"] == "Demo"
    assert course["rating"] == 4.067  # Rounded value
    assert course["price"] == 25.9   # Rounded value
    assert course["owner"]["name"] == "Demo Owner"

# ✅ Test getting all courses
@pytest.mark.asyncio
async def test_get_courses():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get("/course/")
    assert response.status_code == 200
    courses = response.json()
    assert isinstance(courses, list)
    for course in courses:
        assert "_id" in course
        assert "name" in course

# ✅ Test get course by ID
@pytest.mark.asyncio
async def test_get_course_by_id():
    course = await create_course_helper()
    course_id = course["_id"]

    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get(f"/course/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == course_id

# ✅ Test update course
@pytest.mark.asyncio
async def test_update_course():
    course = await create_course_helper()
    course_id = course["_id"]

    update_data = {
        "name": "Updated Course",
        "rating": 4.89,
        "price": 30.456,
        "owner": {
            "id": 50000,
            "name": "Updated Owner"
        },
        "type": "recommended",
        "view": 1000000
    }

    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.put(f"/course/update/{course_id}", json=update_data)
    assert response.status_code == 200
    updated_course = response.json()
    assert updated_course["_id"] == course_id
    assert updated_course["name"] == "Updated Course"
    assert updated_course["rating"] == 4.89
    assert updated_course["price"] == 30.46
    assert updated_course["owner"]["name"] == "Updated Owner"

# ✅ Test delete course
@pytest.mark.asyncio
async def test_delete_course():
    course = await create_course_helper()
    course_id = course["_id"]

    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.delete(f"/course/delete/{course_id}")
        assert response.status_code == 204

        # Verify deletion
        response = await ac.get(f"/course/{course_id}")
        assert response.status_code == 404
