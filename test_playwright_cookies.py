from playwright.sync_api import sync_playwright

def run_playwright_with_cookies():
    cookie_str = "SEARCH_SAMESITE=CgQIv6EB; _gcl_au=1.1.1695937730.1785997533; _ga=GA1.1.2088173675.1785997529; OSID=g.a000BQl_1t4qzUcIvAKseiv0o-bM6hyq4JYlg_uQC0x2Srpzg6mCtBXCyf_ASrRPD7RX1WqIkQACgYKAQ8SARQSFQHGX2Mi8RQJt6An18Z8Pwm1SU4j_hoVAUF8yKoYvdA1H6JUGlbDqsCfTXwr0076; __Secure-OSID=g.a000BQl_1t4qzUcIvAKseiv0o-bM6hyq4JYlg_uQC0x2Srpzg6mCy6BmAD5qYvpD342d-U_aMwACgYKAeYSARQSFQHGX2Micx1_FlRd9Psoi1bWfX53zhoVAUF8yKobF2Y9RnChMXasAsZaLj_N0076; SID=g.a000BQl_1j0NsLWyiKi6uugYJGzLgFOrluWKslV2rtMfm7z-vR8cyIn5v36AGhqf6HCITRD0zQACgYKAZUSARQSFQHGX2MiFslEr-qwSH3ad5MXA0JWnBoVAUF8yKr2xqZbktFTmqFgrHAPhL4-0076; __Secure-1PSID=g.a000BQl_1j0NsLWyiKi6uugYJGzLgFOrluWKslV2rtMfm7z-vR8cKfARprLswR7YnGZqhYbZ6AACgYKAcISARQSFQHGX2Mif_LHds8dbZIp0eo1lPrwBxoVAUF8yKraA9toR5bYyara4DngLq6D0076; __Secure-3PSID=g.a000BQl_1j0NsLWyiKi6uugYJGzLgFOrluWKslV2rtMfm7z-vR8cGXLSnfA0KfrAB1BC44NMyAACgYKARESARQSFQHGX2MiMg7Pv2MvOk2nJstJqU4IMBoVAUF8yKoxSITAwJN3OLpHIUdpEIxG0076; HSID=ARmGWpddUyQ59Ap6d; SSID=AN_WsVqePJwQx1YAH; APISID=5QmfMhwuYXvKIkzu/A3XvctAiKQOkTn_x6; SAPISID=qw9OWs0PUAsbOwts/AGEzfELCLyfCk3Ij6; __Secure-1PAPISID=qw9OWs0PUAsbOwts/AGEzfELCLyfCk3Ij6; __Secure-3PAPISID=qw9OWs0PUAsbOwts/AGEzfELCLyfCk3Ij6; GCL_AW_P=GCL.1786330876.CjwKCAjwk43ABhBIEiwAvvMEBwiianHAFwVNkGRW_jrRCBArGKg6eyApCz6f646nPtNA3EIKJE5SCxoCWEEQAvD_BwE; AEC=AdJVEasLQbu6mhaqsSOufNyU9-ZAuQX09zIexbV0xt-MqWSm2ZJXhh6_eO0; NID=534=V9LQuOz0P-SLZDl5Mxgop_meUbYPbeppWT5beIoTHprG3CxWcFshIaPprYfcESm3Rk85u4bHB8IveRo9TgWa4EUHaLQI8hx_cBwF6AJ5ommDIxYyuz8nW9hG9jWHrDzpDV5UoDw0HL3Fai7_98jr6SQeWnDTvCK3FEcZnIhtERzxWwxXYMphJOz4_DyVjzhEgNIaK-OmgiJAU4ww9R_hvAvHpajYaoMrR66_hRP2JgCPKogjQhnxuQq17PkBkSOJZg2YhuLf1A40q2ZYQ6pqFBM367_293QsexvLKS7XV_gkpHvi-QadRHgVLvFMVQ5N3Ws9I1SoECiT7MdsaTnRUchg_gaHIUCj1JcN7zPt-HT2B7aWHvWSTDi9A7nUWnk306Ye910RZtCkxXRXUGyJIPRJHR8khym0hUdHGBo5m4prqc6eU0qd3SFOxgtxWThQ3OQNnGddUYCRNuO-QXqmKDaT0qoMIZvGf2Li0M3yYDn3NASNTd24OCcfvtg4mWnBl1CHHISyAgt6LVp7CnFd8EPpUdylApGaDTyHBJhgdLaD7f7Gnf4TEK4NiIGOpXPYPosrptulSXvI7IsR51nltuWtYKNHUuCFZ8W0-hkQvrHTKYFtGOMOSVaj2jJl01IvknHrNYx3-6do2Ap6t6OfoKQXJimSVz6krK8NcLErtNPbqVmaR-d5w3blx9twuCSoQLBwXXTCRGlWJyeCRWQeO4-6njzX5n5gWXjyIxR1zKFw2RjfRLqf2u-k7iExsltMVa1F_-MlapBriRgtxvntUr1VJrmuMtoc8hjr09oSAs89kk0tAIXxMlyZ1ac0dZYUn7eBsSrm5B6cmK0W1zXmwBpmbJdnyz4BrtVr-PqNqKqO644tHmJo0sazqQI1j_WlCZKXyHW8F8YqTxxZS_DKbz27prMcq3aCQmnq9bpqr9ziQj8oFLuPYVcDJFCe9KDE5Fh-7Vfc8Ev1nC2pjvgPERisJFNk5gIZ2_zj_cFQxmK_zAMGaCJQ9tm9F7oZ46TEboe6XUKUV2gYlHf5DTWZkLD-DJE3QrxzpWmdx1MDuOjlqyiB2iVm90-nvK5RfBVJINpZbGYmZHKlBCAuy0Gr5Rv0Ki-vp1HoHoPmx8hs6wvMzXZRLKiwZoQ7n6yiQngyobamilATa8F8PQa4i9uTO-9Nt-rwoyHRLdjpWh9iMVOGvYInNjqkN0iFTB7N4D9kEjJfb_o; __Secure-1PSIDTS=sidts-CjcBXMw41cKnpUI2lNH-7Gcc1HNz1v_c-WTINIPwTHYr-WbYTJuYE0FiYTsFNbJXz5DwsGD4Iv6dEAA; __Secure-1PSIDRTS=sidts-CjcBXMw41cKnpUI2lNH-7Gcc1HNz1v_c-WTINIPwTHYr-WbYTJuYE0FiYTsFNbJXz5DwsGD4Iv6dEAA; __Secure-3PSIDTS=sidts-CjcBXMw41cKnpUI2lNH-7Gcc1HNz1v_c-WTINIPwTHYr-WbYTJuYE0FiYTsFNbJXz5DwsGD4Iv6dEAA; __Secure-3PSIDRTS=sidts-CjcBXMw41cKnpUI2lNH-7Gcc1HNz1v_c-WTINIPwTHYr-WbYTJuYE0FiYTsFNbJXz5DwsGD4Iv6dEAA; _ga_W0LDH41ZCB=GS2.1.s1787050230$o20$g1$t1787053790$j44$l0$h0; SIDCC=AKEyXzWNyenIirr43V7SCKngO210fPnCIp4NpuhrehfhYCItDmCQ2MaYqc6fhpK_gSBPyV9WTcs; __Secure-1PSIDCC=AKEyXzXoGZeZimtXNOcceM7MIry0haeUjDIOfBjrsrhBUqSfTsCJmI9Jd_vfyIvWxWlDW_8MgiU; __Secure-3PSIDCC=AKEyXzUkDeh9M2QZkBfdJMUdsvXhurGJDfnIPyfqiu3dHnv7AjqwsNFCQbWsEbQNAh_cG-Uwsw"
    cookies_list = []
    for pair in cookie_str.split(";"):
        if "=" in pair:
            name, value = pair.split("=", 1)
            name = name.strip()
            cookies_list.append({
                "name": name,
                "value": value.strip(),
                "url": "https://notebooklm.google.com/",
                "secure": name.startswith("__Secure-")
            })
            
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies_list)
        
        page = context.new_page()
        page.goto("https://notebooklm.google.com/")
        page.wait_for_load_state("networkidle")
        
        page.screenshot(path="notebooklm_login_test.png")
        print("Screenshot saved to notebooklm_login_test.png. URL is:", page.url)
        browser.close()

if __name__ == "__main__":
    run_playwright_with_cookies()
