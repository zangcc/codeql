package generatedtest;

import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.Callable;
import org.springframework.cache.Cache;


// Test case generated by GenerateFlowTestCase.ql
public class Test {

	public class ValueWrapper extends HashMap<Object,Object> implements Cache.ValueWrapper {
		ValueWrapper(Object element) {
			super();
			this.put(null, element);
		}

		public Object get() { return this.get(null); }
	}

	public class DummyCache implements Cache {
		DummyCache(Object key, Object value) {
			this.put(key, value);
		}

		public void clear() {}
		public void evict(Object key) {}
		public boolean evictIfPresent(Object key) { return false; }
		public Cache.ValueWrapper get(Object key) { return null; }
		public <T> T get(Object key, Callable<T> valueLoader) { return null; }
		public <T> T get(Object key, Class<T> type) { return null; }
		public String getName() { return null; }
		public Object getNativeCache() { return null; }
		//public default boolean invalidate() { return false; }
		public void put(Object key, Object value) {}
		//default Cache.ValueWrapper putIfAbsent(Object key, Object value) { return null; }
	}

	Object getMapKey(Cache.ValueRetrievalException container) { return container.getKey(); }
	Object getMapKey(Cache container) { return ((Map)container.getNativeCache()).keySet().iterator().next(); }
	Object getMapValue(Cache container) { return container.get(null, (Class)null); }
	Object getMapValue(Cache.ValueWrapper container) { return container.get(); }
	Object source() { return null; }
	void sink(Object o) { }

	public void test() {

		{
			// "org.springframework.cache;Cache$ValueRetrievalException;false;ValueRetrievalException;;;Argument[0];MapKey of Argument[this];value;manual"
			Cache.ValueRetrievalException out = null;
			Object in = source();
			out = new Cache.ValueRetrievalException(in, null, null);
			sink(getMapKey(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache$ValueRetrievalException;false;getKey;;;MapKey of Argument[this];ReturnValue;value;manual"
			Object out = null;
			Cache.ValueRetrievalException in = new Cache.ValueRetrievalException(source(), null, null);
			out = in.getKey();
			sink(out); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache$ValueWrapper;true;get;;;MapValue of Argument[this];ReturnValue;value;manual"
			Object out = null;
			Cache.ValueWrapper in = new ValueWrapper(source());
			out = in.get();
			sink(out); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;get;(Object);;MapValue of Argument[this];MapValue of ReturnValue;value;manual"
			Cache.ValueWrapper out = null;
			Cache in = new DummyCache(null, source());
			out = in.get(null);
			sink(getMapValue(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;get;(Object,Callable);;MapValue of Argument[this];ReturnValue;value;manual"
			Object out = null;
			Cache in = new DummyCache(null, source());
			out = in.get(null, (Callable)null);
			sink(out); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;get;(Object,Class);;MapValue of Argument[this];ReturnValue;value;manual"
			Object out = null;
			Cache in = new DummyCache(null, source());
			out = in.get(null, (Class)null);
			sink(out); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;getNativeCache;;;MapKey of Argument[this];MapKey of ReturnValue;value;manual"
			Object out = null;
			Cache in = new DummyCache(source(), null);
			out = in.getNativeCache();
			sink(getMapKey((Cache)out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;getNativeCache;;;MapValue of Argument[this];MapValue of ReturnValue;value;manual"
			Object out = null;
			Cache in = new DummyCache(null, source());
			out = in.getNativeCache();
			sink(getMapValue((Cache)out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;put;;;Argument[0];MapKey of Argument[this];value;manual"
			Cache out = null;
			Object in = source();
			out.put(in, null);
			sink(getMapKey(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;put;;;Argument[1];MapValue of Argument[this];value;manual"
			Cache out = null;
			Object in = source();
			out.put(null, in);
			sink(getMapValue(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;putIfAbsent;;;Argument[0];MapKey of Argument[this];value;manual"
			Cache out = null;
			Object in = source();
			out.putIfAbsent(in, null);
			sink(getMapKey(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;putIfAbsent;;;Argument[1];MapValue of Argument[this];value;manual"
			Cache out = null;
			Object in = source();
			out.putIfAbsent(null, in);
			sink(getMapValue(out)); // $hasValueFlow
		}
		{
			// "org.springframework.cache;Cache;true;putIfAbsent;;;MapValue of Argument[this];MapValue of ReturnValue;value;manual"
			Cache.ValueWrapper out = null;
			Cache in = new DummyCache(null, source());
			out = in.putIfAbsent(null, null);
			sink(getMapValue(out)); // $hasValueFlow
		}

	}

}
