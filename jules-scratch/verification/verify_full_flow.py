from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Waiter login
    page.goto("http://localhost:8080/login/")
    page.fill("#username", "waiter")
    page.fill("#password", "waiter")
    page.click("button[type=submit]")
    page.wait_for_timeout(2000)

    # Create order
    page.goto("http://localhost:8080/waiter/")
    page.wait_for_selector(".table", timeout=60000)
    page.click(".table")
    page.click(".menu-item")
    page.click("#place-order")
    page.screenshot(path="jules-scratch/verification/order_placed.png")

    # Kitchen login
    page.goto("http://localhost:8080/login/")
    page.fill("#username", "kitchen")
    page.fill("#password", "kitchen")
    page.click("button[type=submit]")
    page.wait_for_timeout(2000)
    page.goto("http://localhost:8080/kitchen/")
    page.wait_for_selector(".order-card", timeout=60000)
    page.screenshot(path="jules-scratch/verification/kitchen_order.png")

    # Update order status
    page.select_option(".order-card select", "in_progress")
    page.wait_for_timeout(1000) # Wait for websocket to update
    page.screenshot(path="jules-scratch/verification/kitchen_status_updated.png")

    # Waiter login again
    page.goto("http://localhost:8080/login/")
    page.fill("#username", "waiter")
    page.fill("#password", "waiter")
    page.click("button[type=submit]")
    page.wait_for_timeout(2000)
    page.goto("http://localhost:8080/waiter/")
    page.wait_for_selector(".table", timeout=60000)

    # Generate bill
    page.click(".table")
    page.click("#generate-bill")
    page.wait_for_selector("#table-bills div")
    page.screenshot(path="jules-scratch/verification/bill_generated.png")

    # Pay bill
    page.click("#table-bills button:first-child")
    page.wait_for_timeout(1000) # Wait for UI to update
    page.screenshot(path="jules-scratch/verification/bill_paid.png")

    # Admin login
    page.goto("http://localhost:8080/login/")
    page.fill("#username", "admin")
    page.fill("#password", "admin")
    page.click("button[type=submit]")
    page.wait_for_timeout(2000)
    page.goto("http://localhost:8080/admin/")
    page.wait_for_selector("#sales-report", timeout=60000)
    page.screenshot(path="jules-scratch/verification/admin_analytics.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
