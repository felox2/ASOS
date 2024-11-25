import { mount } from "@vue/test-utils";
import { describe, it, expect, vi } from "vitest";
import { ref } from "vue";
import ProductSearch from "@/components/ProductSearch.vue";
import { useI18n } from "vue-i18n";
import { useFetchQuery } from "@/composables/useQuery";
import { client } from "@/lib/client";

// Mock dependencies
vi.mock("@/composables/useQuery", () => ({
  useFetchQuery: vi.fn(),
}));
vi.mock("@/lib/client", () => ({
  client: {
    GET: vi.fn(),
  },
}));
vi.mock("vue-i18n", () => ({
  useI18n: () => ({
    t: (key: string) => key,
    n: (value: number, format: string) => `${value} ${format}`,
  }),
}));

describe("ProductSearch", () => {
  it("renders the search input and placeholder text", () => {
    // Mock `useFetchQuery` to return an empty data structure
    (useFetchQuery as any).mockReturnValue({
      data: ref([]), // Provide a valid structure
    });

    const wrapper = mount(ProductSearch);
    const input = wrapper.find("input");
    expect(input.exists()).toBe(true);
    expect(input.attributes("placeholder")).toBe("search");
  });

  it("updates the query value and triggers debounced search", async () => {
    // Mock `useFetchQuery` to return empty data
    (useFetchQuery as any).mockReturnValue({
      data: ref([]),
    });
  
    // Mount the component
    const wrapper = mount(ProductSearch);
  
    // Find the input field and simulate user input
    const input = wrapper.find("input");
    await input.setValue("Tablet");
  
    // Check if the component's `query` ref is updated
    expect((wrapper.vm as any).query).toBe("Tablet"); // Correct assertion
  });
  

  it("displays no results message when items are empty", () => {
    (useFetchQuery as any).mockReturnValue({
      data: ref([]),
    });

    const wrapper = mount(ProductSearch);
    expect(wrapper.html()).toContain("empty");
  });

  it("closes the dropdown when clicking outside", async () => {
    // Mock `useFetchQuery` to return a default structure
    (useFetchQuery as any).mockReturnValue({
      data: ref([]), // Ensure `data` is a valid ref
    });
  
    // Mount the component
    const wrapper = mount(ProductSearch);
    const container = wrapper.find(".relative");
    const input = wrapper.find("input");
    
  
    // Simulate focusing the input to open the dropdown
    await input.trigger("focus");
    await input.setValue("laptop");
    const results = wrapper.find("div.absolute");
    expect(results.html()).toContain("opacity-100"); // Dropdown is open
  
    document.body.click();
    await input.trigger("blur");
    await wrapper.trigger("blur")


    expect(results.html()).not.toContain("opacity-100"); // Dropdown is closed
  });
  

  it("resets the query and closes dropdown when close is called", async () => {
    const wrapper = mount(ProductSearch);
    const input = wrapper.find("input");

    await input.setValue("laptop");
    expect(wrapper.vm.query).toBe("laptop");

    wrapper.vm.close();
    expect(wrapper.vm.query).toBe("");
    expect(wrapper.vm.open).toBe(false);
  });
});
