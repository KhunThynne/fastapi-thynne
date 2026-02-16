import asyncio
import os
import sys

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

from app.api.graphql import schema


async def verify_graphql() -> None:
    print("Verifying GraphQL Schema...")

    # Test Query
    query = """
        query {
            getUsers {
                id
                username
                email
            }
        }
    """
    print("\nExecuting Query:")
    result = await schema.execute(query)
    if result.errors:
        print("Query Errors:", result.errors)
        sys.exit(1)
    print("Query Result:", result.data)

    # Test Mutation
    mutation = """
        mutation {
            createUser(username: "testuser", email: "test@example.com") {
                id
                username
                email
            }
        }
    """
    print("\nExecuting Mutation:")
    result = await schema.execute(mutation)
    if result.errors:
        print("Mutation Errors:", result.errors)
        sys.exit(1)
    print("Mutation Result:", result.data)

    print("\nVerification Successful!")


if __name__ == "__main__":
    asyncio.run(verify_graphql())
