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
    page.wait_for_selector(".table")
    page.click(".table")
    page.click(".menu-item")
    page.click("#place-order")
    page.screenshot(path="jules-scratch/verification/order_placed_final.png")

    # Generate bill
    page.click("#generate-bill")
    page.wait_for_selector("#table-bills div")
    page.screenshot(path="jules-scratch/verification/bill_generated_final.png")

    # Pay bill
    page.click("#table-bills button:first-child")
    page.wait_for_timeout(1000) # Wait for UI to update
    page.screenshot(path="jules-scratch/verification/bill_paid_final.png")

    # Attempt to generate another bill
    page.click("#generate-bill")
    page.on("dialog", lambda dialog: dialog.accept())
    page.screenshot(path="jules-scratch/verification/generate_bill_fail.png")

    # Admin login
    page.goto("http://localhost:8080/login/")
    page.fill("#username", "admin")
    page.fill("#password", "admin")
    page.click("button[type=submit]")
    page.wait_for_timeout(2000)
    page.goto("http://localhost:8080/admin/")
    page.wait_for_selector("#sales-report")
    page.screenshot(path="jules-scratch/verification/admin_analytics_final.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
