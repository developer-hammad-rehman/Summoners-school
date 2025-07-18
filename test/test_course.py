import pytest
from httpx import AsyncClient

base_url = "http://localhost:8000"

async def create_course_helper():
    data = {
        "name": "Demo",
        "description": "Demo",
        "hours": 10,
        "imageLink": "https://demo.example.com/images/demo.jpg",
        "shortVideo": "https://demo.example.com/videos/demo.mp4",
    }
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/course/create", json=data)
        assert response.status_code == 200
        return response.json()

@pytest.mark.asyncio
async def test_create_course():
    course = await create_course_helper()
    assert "_id" in course
    assert isinstance(course["_id"], str)
    assert len(course["_id"]) == 24
    assert course["name"] == "Demo"

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

@pytest.mark.asyncio
async def test_get_course_by_id():
    course = await create_course_helper()
    course_id = course["_id"]

    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get(f"/course/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == course_id

@pytest.mark.asyncio
async def test_update_course():
    course = await create_course_helper()
    course_id = course["_id"]

    update_data = {
        "name": "Updated Course",
        "hours": 25
    }

    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.put(f"/course/update/{course_id}", json=update_data)
    assert response.status_code == 200
    updated_course = response.json()
    assert updated_course["_id"] == course_id
    assert updated_course["name"] == update_data["name"]
    assert updated_course["hours"] == update_data["hours"]

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
