from typing import cast
from fastmcp import FastMCP, Context
from mcp.types import TextContent


mcp = FastMCP(
    "BetterCodeMcp",
    dependencies=[],
)

@mcp.prompt()
def check_code_quality_prompt(code: str) -> str:
    """Check Code Quality Prompt"""
    return  """
## Code Quality - Cognitive Load Checklist

**Clarity & Simplicity:**

*   **Complex Conditionals:** Are there complex `if` statements?
    *   **Action:** Introduce intermediate variables with meaningful names to simplify conditions.
*   **Nested Ifs:** Is there deep nesting of `if` statements?
    *   **Action:** Consider using early returns/guard clauses to focus on the "happy path."
*   **Naming:** Are variable, function, and class names clear, descriptive, and unambiguous?
*   **Language Features:** Am I using complex or obscure language features where simpler alternatives exist?
    *   **Action:** Prefer straightforward and commonly understood language constructs. Limit the number of choices to avoid confusion.

**Structure & Design:**

*   **Inheritance:** Is inheritance being used excessively, leading to a complex hierarchy?
    *   **Action:** Prefer composition over inheritance.
*   **Module Depth:**
    *   Are there too many small, shallow methods, classes, or modules where their interfaces are complex relative to the functionality they provide?
    *   **Action:** Aim for "deep modules" – simple interfaces hiding complex functionality. Avoid an excessive number of interconnected shallow modules.
*   **Single Responsibility Principle (SRP):** Is the module responsible to more than one user or stakeholder (i.e., a change for one stakeholder might inadvertently affect another)?
    *   **Action:** Ensure a module has a single, clear reason to change, tied to a specific user or stakeholder need, rather than just "doing one thing" vaguely.
*   **Microservices:** If using microservices, are they overly granular ("shallow microservices") leading to a distributed monolith?
    *   **Action:** Ensure microservices represent genuinely distinct, deep logical boundaries. Consider if a well-structured monolith or "macroservices" would be simpler. Make decisions about network layers as late as responsibly possible.
*   **DRY (Don't Repeat Yourself):** Is DRY being overused, leading to tight coupling between unrelated components or unnecessary abstractions?
    *   **Action:** A little copying can be better than a little dependency. Avoid importing large libraries for trivial functions.
*   **Framework Coupling:** Is the business logic tightly coupled to a specific framework, making it hard for new developers to understand or for the system to adapt?
    *   **Action:** Keep business logic separate from framework concerns. Use frameworks in a library-like fashion.
*   **Layered Architecture:** Are there too many layers of abstraction that don't provide significant practical benefits (e.g., for extensibility or testability) but increase the effort to trace logic?
    *   **Action:** Add abstraction layers only when justified for practical reasons. Focus on fundamental principles like dependency inversion and keeping business logic independent of low-level modules. Avoid layers for the sake of "architecture."

**External Interactions & Conventions:**

*   **Numeric Statuses/Codes (e.g., HTTP, DB):** Are numeric codes used that require a separate mapping to understand their meaning (e.g., custom HTTP status code meanings)?
    *   **Action:** Prefer self-describing string codes in response bodies or enums with clear names. Abstract business details away from transfer protocols.
*   **DDD (Domain-Driven Design):** If applying DDD, is the focus on concrete solution-space techniques (folder structures, specific patterns) rather than understanding the problem space (ubiquitous language, bounded contexts)?
    *   **Action:** Ensure DDD is used to improve communication and understanding of the domain, not just to implement specific technical patterns that might be subjective or increase cognitive load.

**General Maintainability:**

*   **Onboarding:** How quickly can a new developer understand this code and start contributing? Could a junior developer identify mentally demanding areas?
*   **Familiarity vs. Simplicity:** Is the code easy to understand because it's genuinely simple, or just because I'm familiar with its complexities?
*   **Overall Question:** Does this code make developers think unnecessarily hard to understand or modify it?

**Goal: Reduce any cognitive load above and beyond what is intrinsic to the problem being solved.**


""" + "## Input Code:\n\n" + code



@mcp.tool()
async def check_code_quality(code: str, ctx: Context) -> str:
    await ctx.info("begin to prompt")
    prompt = check_code_quality_prompt(code)
    call_result = await ctx.sample(prompt)
    return cast(TextContent, call_result).text



if __name__ == "__main__":
    mcp.run(transport="stdio")
